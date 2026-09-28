from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .participation import Participation


class Project(SQLModel, table=True):
    slug: str = Field(primary_key=True)
    name: str
    state: str
    description: Optional[str] = None

    participations: list["Participation"] = Relationship(back_populates="project")
