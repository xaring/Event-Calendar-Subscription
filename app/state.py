import reflex as rx
import bcrypt
import os
from typing import TypedDict
from reflex_google_auth import GoogleAuthState
import datetime
from sqlmodel import select, and_
from .models import User


class LocalAuthState(rx.State):
    is_authenticated: bool = False
    authenticated_user: dict | None = None
    error_message: str = ""
    success_message: str = ""

    def _get_user_by_email(self, email: str) -> User | None:
        with rx.session() as session:
            return session.exec(select(User).where(User.email == email)).first()

    def _get_user_by_google_id(self, google_id: str) -> User | None:
        with rx.session() as session:
            return session.exec(select(User).where(User.google_id == google_id)).first()

    @rx.event
    def register(self, form_data: dict):
        email = form_data.get("email")
        password = form_data.get("password")
        name = form_data.get("name")
        confirm_password = form_data.get("confirm_password")
        if not all([email, password, name, confirm_password]):
            self.error_message = "All fields are required."
            return
        if password != confirm_password:
            self.error_message = "Passwords do not match."
            return
        if self._get_user_by_email(email):
            self.error_message = "User with this email already exists."
            return
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        with rx.session() as session:
            new_user = User(
                email=email, password=hashed_password, name=name, role="user"
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            self.authenticated_user = new_user.dict()
            self.is_authenticated = True
            self.error_message = ""
        return rx.redirect("/")

    @rx.event
    def login(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.error_message = "Email and password are required."
            return
        user = self._get_user_by_email(email)
        if not user or not user.password:
            self.error_message = "Invalid email or password."
            return
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            self.authenticated_user = user.dict()
            self.is_authenticated = True
            self.error_message = ""
            return rx.redirect("/")
        else:
            self.error_message = "Invalid email or password."

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.authenticated_user = None
        self.error_message = ""
        self.success_message = ""
        yield MyGoogleAuthState.logout

    @rx.var
    def is_admin(self) -> bool:
        return (
            self.authenticated_user is not None
            and self.authenticated_user.get("role") == "admin"
        )

    @rx.event
    def change_password(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        current_password = form_data.get("current_password")
        new_password = form_data.get("new_password")
        confirm_new_password = form_data.get("confirm_new_password")
        if not all([current_password, new_password, confirm_new_password]):
            self.error_message = "All fields are required."
            return
        if new_password != confirm_new_password:
            self.error_message = "New passwords do not match."
            return
        with rx.session() as session:
            user = session.get(User, self.authenticated_user["id"])
            if (
                not user
                or not user.password
                or (
                    not bcrypt.checkpw(
                        current_password.encode("utf-8"), user.password.encode("utf-8")
                    )
                )
            ):
                self.error_message = "Invalid current password."
                return
            hashed_password = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            user.password = hashed_password
            session.add(user)
            session.commit()
        self.success_message = "Password changed successfully!"


class MyGoogleAuthState(GoogleAuthState):
    @rx.var(cache=True)
    def client_id(self) -> str:
        return os.getenv("GOOGLE_CLIENT_ID", "")

    @rx.event
    async def on_success(self, id_token: dict):
        local_auth_state = await self.get_state(LocalAuthState)
        google_id = id_token.get("sub")
        email = id_token.get("email")
        name = id_token.get("name")
        user = local_auth_state._get_user_by_google_id(google_id)
        if not user:
            user = local_auth_state._get_user_by_email(email)
            if user:
                user.google_id = google_id
                with rx.session() as session:
                    session.add(user)
                    session.commit()
                    session.refresh(user)
            else:
                with rx.session() as session:
                    new_user = User(
                        email=email,
                        password=None,
                        name=name,
                        google_id=google_id,
                        role="user",
                    )
                    session.add(new_user)
                    session.commit()
                    session.refresh(new_user)
                    user = new_user
        local_auth_state.authenticated_user = user.dict()
        local_auth_state.is_authenticated = True
        return rx.redirect("/")


class GoogleAuthInfo(TypedDict):
    token_is_valid: bool
    tokeninfo: dict
    user_name: str
    user_email: str