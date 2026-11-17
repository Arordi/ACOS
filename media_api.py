from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from models.media import MediaFile
from models.project import Project
from schemas.media import MediaFileResponse


router = APIRouter(
    prefix="/api/media",
    tags=["Media"],
)


@router.get(
    "/project/{project_id}",
    response_model=list[MediaFileResponse],
)
def list_project_media(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return db.query(MediaFile).filter(
        MediaFile.project_id == project_id
    ).all()
