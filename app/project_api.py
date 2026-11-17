from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.database import get_db
from models.project import Project
from schemas.project import ProjectCreate, ProjectResponse


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)


# ============================================================
# CREATE PROJECT
# ============================================================

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new ACOS project.
    """

    try:
        project = Project(
            name=project_data.name,
            description=project_data.description,
            project_type=project_data.project_type,
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        return project

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Project could not be created.",
        )


# ============================================================
# LIST PROJECTS
# ============================================================

@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_projects(
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of projects to skip.",
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
        description="Maximum number of projects to return.",
    ),
    db: Session = Depends(get_db),
):
    """
    Return projects.

    Newest projects are returned first.

    Pagination:
        ?skip=0&limit=50
    """

    try:
        return (
            db.query(Project)
            .order_by(Project.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Projects could not be loaded.",
        )


# ============================================================
# GET SINGLE PROJECT
# ============================================================

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    """
    Return one project by ID.
    """

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Project not found.",
                "project_id": project_id,
            },
        )

    return project


# ============================================================
# UPDATE PROJECT
# ============================================================

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
):
    """
    Update an existing ACOS project.
    """

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Project not found.",
                "project_id": project_id,
            },
        )

    try:
        project.name = project_data.name
        project.description = project_data.description
        project.project_type = project_data.project_type

        db.commit()
        db.refresh(project)

        return project

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Project could not be updated.",
        )


# ============================================================
# DELETE PROJECT
# ============================================================

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an existing ACOS project.
    """

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Project not found.",
                "project_id": project_id,
            },
        )

    try:
        db.delete(project)
        db.commit()

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Project could not be deleted.",
        )

    return None
