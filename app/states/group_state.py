import reflex as rx
from sqlmodel import select
from app.models import Group, UserGroup, User, Event
from app.state import LocalAuthState


class GroupState(rx.State):
    groups: list[Group] = []
    user_groups: list[Group] = []
    error_message: str = ""
    success_message: str = ""

    @rx.event
    def load_groups(self):
        with rx.session() as session:
            self.groups = session.exec(select(Group).order_by(Group.name)).all()

    @rx.event
    async def load_user_groups(self):
        local_auth = await self.get_state(LocalAuthState)
        if not local_auth.is_authenticated or not local_auth.authenticated_user:
            self.user_groups = []
            return
        user_id = local_auth.authenticated_user.get("id")
        with rx.session() as session:
            user_group_links = session.exec(
                select(UserGroup).where(UserGroup.user_id == user_id)
            ).all()
            group_ids = [ug.group_id for ug in user_group_links]
            if group_ids:
                self.user_groups = session.exec(
                    select(Group).where(Group.id.in_(group_ids))
                ).all()
            else:
                self.user_groups = []

    @rx.event
    def create_group(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        name = form_data.get("name")
        description = form_data.get("description")
        if not name:
            self.error_message = "Group name is required."
            return
        with rx.session() as session:
            existing_group = session.exec(
                select(Group).where(Group.name == name)
            ).first()
            if existing_group:
                self.error_message = "A group with this name already exists."
                return
            new_group = Group(name=name, description=description)
            session.add(new_group)
            session.commit()
            self.success_message = "Group created successfully!"
        return GroupState.load_groups

    @rx.event
    def delete_group(self, group_id: int):
        with rx.session() as session:
            user_group_links = session.exec(
                select(UserGroup).where(UserGroup.group_id == group_id)
            ).all()
            for link in user_group_links:
                session.delete(link)
            events_in_group = session.exec(
                select(Event).where(Event.group_id == group_id)
            ).all()
            for event in events_in_group:
                event.group_id = None
                session.add(event)
            group = session.get(Group, group_id)
            if group:
                session.delete(group)
                session.commit()
                self.success_message = "Group deleted successfully!"
        return GroupState.load_groups