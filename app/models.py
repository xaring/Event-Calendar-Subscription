import datetime
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    name: str
    role: str = "user"
    google_id: str | None = Field(default=None, unique=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    groups: list["UserGroup"] = Relationship(back_populates="user")
    event_signups: list["EventSignup"] = Relationship(back_populates="user")
    payments: list["Payment"] = Relationship(back_populates="user")


class Group(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: str | None = None
    users: list["UserGroup"] = Relationship(back_populates="group")
    events: list["Event"] = Relationship(back_populates="group")


class UserGroup(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)
    user: "User" = Relationship(back_populates="groups")
    group: "Group" = Relationship(back_populates="users")


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    group_id: int | None = Field(foreign_key="group.id", default=None)
    group: Group | None = Relationship(back_populates="events")
    signups: list["EventSignup"] = Relationship(back_populates="event")


class EventSignup(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    event_id: int = Field(foreign_key="event.id")
    signup_time: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    user: "User" = Relationship(back_populates="event_signups")
    event: "Event" = Relationship(back_populates="signups")


class Payment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    amount: float
    payment_date: datetime.date
    payment_type: str
    months_covered: int = 1
    user: "User" = Relationship(back_populates="payments")