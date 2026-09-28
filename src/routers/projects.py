from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database import get_session
from src.models import Project, Participation, Member

router = APIRouter()


@router.post("/projects")
def create_project(project: Project, session: Session = Depends(get_session)):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/projects")
def list_projects(session: Session = Depends(get_session)):
    return session.exec(select(Project)).all()


@router.get("/projects/{slug}")
def get_project(slug: str, session: Session = Depends(get_session)):
    project = session.get(Project, slug)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/projects/{slug}/members")
def get_project_members(slug: str, session: Session = Depends(get_session)):
    statement = (
        select(Member)
        .join(Participation)
        .where(Participation.project_slug == slug)
    )
    return session.exec(statement).all()

@router.get("/projects/{slug}/full")
def get_project_full(slug: str, session: Session = Depends(get_session)):
    project = session.get(Project, slug)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    members = session.exec(
        select(Member).join(Participation).where(Participation.project_slug == slug)
    ).all()

    return {
        "slug": project.slug,
        "name": project.name,
        "state": project.state,
        "description": project.description,
        "members": [{"ist_id": m.ist_id, "name": m.name} for m in members],
    }


@router.get("/projects-full")
def list_projects_full(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    result = []
    for project in projects:
        members = session.exec(
            select(Member).join(Participation).where(Participation.project_slug == project.slug)
        ).all()
        result.append({
            "slug": project.slug,
            "name": project.name,
            "state": project.state,
            "description": project.description,
            "members": [{"ist_id": m.ist_id, "name": m.name} for m in members],
        })
    return result
