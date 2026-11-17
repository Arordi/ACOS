from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.project import Project
from schemas.project import ProjectCreate, ProjectResponse


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    project = Project(
        name=project_data.name,
        description=project_data.description,
        project_type=project_data.project_type,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    db: Session = Depends(get_db),
):
    return db.query(Project).all()
