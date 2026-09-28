from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

if TYPE_CHECKING:
    from .participation import Participation


class Member(SQLModel, table=True):
    ist_id: str = Field(primary_key=True)
    name: str
    email: str
    course: Optional[str] = None
    role: str
    teams: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    bio: Optional[str] = None
    github: Optional[str] = None

    participations: list["Participation"] = Relationship(back_populates="member")
