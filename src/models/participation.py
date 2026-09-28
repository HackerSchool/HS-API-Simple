from sqlmodel import SQLModel, Field, Relationship
from .member import Member
from .project import Project


class Participation(SQLModel, table=True):
    member_ist_id: str = Field(foreign_key="member.ist_id", primary_key=True)
    project_slug: str = Field(foreign_key="project.slug", primary_key=True)

    member: Member = Relationship(back_populates="participations")
    project: Project = Relationship(back_populates="participations")
