import reflex as rx
import datetime
import logging
from sqlmodel import select, delete
from app.models import Event, EventSignup, Group, UserGroup
from app.state import LocalAuthState


class EventState(rx.State):
    events: list[Event] = []
    my_events: list[Event] = []
    groups: list[Group] = []
    error_message: str = ""
    success_message: str = ""

    @rx.event
    def load_events(self):
        with rx.session() as session:
            self.events = session.exec(select(Event).order_by(Event.start_time)).all()
            self.groups = session.exec(select(Group)).all()

    @rx.event
    def create_event(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        title = form_data.get("title")
        description = form_data.get("description")
        start_time_str = form_data.get("start_time")
        end_time_str = form_data.get("end_time")
        group_id = form_data.get("group_id")
        if not all([title, description, start_time_str, end_time_str]):
            self.error_message = "All fields except group are required."
            return
        try:
            start_time = datetime.datetime.fromisoformat(start_time_str)
            end_time = datetime.datetime.fromisoformat(end_time_str)
        except ValueError as e:
            logging.exception(f"Error parsing datetime: {e}")
            self.error_message = "Invalid datetime format."
            return
        with rx.session() as session:
            new_event = Event(
                title=title,
                description=description,
                start_time=start_time,
                end_time=end_time,
                group_id=int(group_id) if group_id and group_id != "" else None,
            )
            session.add(new_event)
            session.commit()
            self.success_message = "Event created successfully!"
        return EventState.load_events

    @rx.event
    def delete_event(self, event_id: int):
        with rx.session() as session:
            signups = session.exec(
                select(EventSignup).where(EventSignup.event_id == event_id)
            ).all()
            for signup in signups:
                session.delete(signup)
            event = session.get(Event, event_id)
            if event:
                session.delete(event)
                session.commit()
                self.success_message = "Event deleted successfully!"
        return EventState.load_events

    @rx.event
    async def signup_for_event(self, event_id: int):
        local_auth = await self.get_state(LocalAuthState)
        if not local_auth.is_authenticated:
            return rx.redirect("/login")
        user_id = local_auth.authenticated_user["id"]
        with rx.session() as session:
            existing_signup = session.exec(
                select(EventSignup).where(
                    EventSignup.user_id == user_id, EventSignup.event_id == event_id
                )
            ).first()
            if existing_signup:
                self.error_message = "You are already signed up for this event."
                return rx.toast.error("You are already signed up for this event.")
            new_signup = EventSignup(user_id=user_id, event_id=event_id)
            session.add(new_signup)
            session.commit()
            self.success_message = "Successfully signed up for the event!"
        return rx.toast.success("Successfully signed up for the event!")

    @rx.event
    async def cancel_signup(self, event_id: int):
        local_auth = await self.get_state(LocalAuthState)
        if not local_auth.is_authenticated:
            return rx.redirect("/login")
        user_id = local_auth.authenticated_user["id"]
        with rx.session() as session:
            signup = session.exec(
                select(EventSignup).where(
                    EventSignup.user_id == user_id, EventSignup.event_id == event_id
                )
            ).first()
            if signup:
                session.delete(signup)
                session.commit()
                self.success_message = "Successfully canceled signup."
                return EventState.load_my_events
            else:
                self.error_message = "Signup not found."

    @rx.event
    async def load_my_events(self):
        local_auth = await self.get_state(LocalAuthState)
        if not local_auth.is_authenticated:
            return
        user_id = local_auth.authenticated_user["id"]
        with rx.session() as session:
            signed_up_event_ids = session.exec(
                select(EventSignup.event_id).where(EventSignup.user_id == user_id)
            ).all()
            self.my_events = session.exec(
                select(Event)
                .where(Event.id.in_(signed_up_event_ids))
                .order_by(Event.start_time)
            ).all()