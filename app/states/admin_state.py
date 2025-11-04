import reflex as rx
from sqlmodel import select as sqlmodel_select
from app.models import User, Group, Event


class AdminState(rx.State):
    users: list[User] = []
    groups: list[Group] = []
    events: list[Event] = []

    @rx.event
    def load_dashboard_data(self):
        with rx.session() as session:
            self.users = session.exec(sqlmodel_select(User)).all()
            self.groups = session.exec(sqlmodel_select(Group)).all()
            self.events = session.exec(sqlmodel_select(Event)).all()