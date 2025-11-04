import reflex as rx
from sqlmodel import select
from app.models import Payment, User
from app.state import LocalAuthState
import datetime
import logging


class PaymentState(rx.State):
    payments: list[Payment] = []
    users_with_payment_status: list[dict] = []
    all_users: list[User] = []

    @rx.event
    async def load_my_payments(self):
        local_auth = await self.get_state(LocalAuthState)
        if not local_auth.is_authenticated:
            return
        user_id = local_auth.authenticated_user["id"]
        with rx.session() as session:
            self.payments = session.exec(
                select(Payment)
                .where(Payment.user_id == user_id)
                .order_by(Payment.payment_date.desc())
            ).all()

    @rx.event
    async def load_all_users_and_payments(self):
        local_auth = await self.get_state(LocalAuthState)
        if not local_auth.is_admin:
            return
        with rx.session() as session:
            self.all_users = session.exec(select(User)).all()
            users_payments = []
            for user in self.all_users:
                last_payment = session.exec(
                    select(Payment)
                    .where(Payment.user_id == user.id)
                    .order_by(Payment.payment_date.desc())
                ).first()
                days_left = "N/A"
                status = "No payments"
                if last_payment:
                    expiry_date = last_payment.payment_date + datetime.timedelta(
                        days=30 * last_payment.months_covered
                    )
                    delta = expiry_date - datetime.date.today()
                    days_left = delta.days
                    if days_left < 0:
                        status = "Overdue"
                    elif days_left <= 7:
                        status = "Due soon"
                    else:
                        status = "Current"
                users_payments.append(
                    {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "last_payment_date": last_payment.payment_date.isoformat()
                        if last_payment
                        else "N/A",
                        "months_covered": last_payment.months_covered
                        if last_payment
                        else "N/A",
                        "days_until_due": days_left,
                        "status": status,
                    }
                )
            self.users_with_payment_status = users_payments

    @rx.event
    async def record_payment(self, form_data: dict):
        local_auth = await self.get_state(LocalAuthState)
        if not local_auth.is_admin:
            yield rx.toast.error("You are not authorized to perform this action.")
            return
        user_id = form_data.get("user_id")
        amount = form_data.get("amount")
        payment_date_str = form_data.get("payment_date")
        months_covered = form_data.get("months_covered")
        if not all([user_id, amount, payment_date_str, months_covered]):
            yield rx.toast.error("All fields are required.")
            return
        try:
            user_id = int(user_id)
            amount = float(amount)
            months_covered = int(months_covered)
            payment_date = datetime.datetime.fromisoformat(payment_date_str).date()
        except (ValueError, TypeError) as e:
            logging.exception(f"Error processing payment form: {e}")
            yield rx.toast.error("Invalid data format.")
            return
        with rx.session() as session:
            new_payment = Payment(
                user_id=user_id,
                amount=amount,
                payment_date=payment_date,
                months_covered=months_covered,
                payment_type="manual",
            )
            session.add(new_payment)
            session.commit()
        yield rx.toast.success("Payment recorded successfully.")
        yield PaymentState.load_all_users_and_payments