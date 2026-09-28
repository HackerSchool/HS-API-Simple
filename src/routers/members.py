from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select
import os, shutil

from src.database import get_session
from src.models import Member, Participation, Project

router = APIRouter()

UPLOAD_DIR = "uploads/members"
DEFAULT_IMAGE = "uploads/defaults/default-member.png"


@router.post("/members")
def create_member(member: Member, session: Session = Depends(get_session)):
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


@router.get("/members")
def list_members(session: Session = Depends(get_session)):
    return session.exec(select(Member)).all()

@router.post("/members/{ist_id}/image")
async def upload_member_image(ist_id: str, file: UploadFile, session: Session = Depends(get_session)):
    member = session.get(Member, ist_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=422, detail="Only jpg/png allowed")

    ext = ".jpg" if file.content_type == "image/jpeg" else ".png"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    path = os.path.join(UPLOAD_DIR, f"{ist_id}{ext}")

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"description": "Image uploaded successfully", "ist_id": ist_id}


@router.get("/members/{ist_id}/image")
async def get_member_image(ist_id: str):
    for ext in (".jpg", ".jpeg", ".png"):
        path = os.path.join(UPLOAD_DIR, f"{ist_id}{ext}")
        if os.path.exists(path):
            return FileResponse(path)
    return FileResponse(DEFAULT_IMAGE)

@router.get("/members/{ist_id}")
def get_member(ist_id: str, session: Session = Depends(get_session)):
    member = session.get(Member, ist_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.get("/members/{ist_id}/projects")
def get_member_projects(ist_id: str, session: Session = Depends(get_session)):
    statement = (
        select(Project)
        .join(Participation)
        .where(Participation.member_ist_id == ist_id)
    )
    return session.exec(statement).all()


@router.post("/members/{ist_id}/projects/{slug}")
def add_member_to_project(ist_id: str, slug: str, session: Session = Depends(get_session)):
    member = session.get(Member, ist_id)
    project = session.get(Project, slug)
    if not member or not project:
        raise HTTPException(status_code=404, detail="Member or project not found")

    participation = Participation(member_ist_id=ist_id, project_slug=slug)
    session.add(participation)
    session.commit()
    return {"description": "Member added to project", "ist_id": ist_id, "slug": slug}
