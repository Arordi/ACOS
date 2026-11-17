import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from core.config import settings
from core.database import get_db
from models.media import MediaFile
from models.project import Project
from schemas.media import MediaFileResponse


router = APIRouter(
    prefix="/api/media",
    tags=["Media"],
)


STORAGE_DIR = "storage"

ALLOWED_FILE_TYPES = {
    "video": {
        "video/mp4",
        "video/mpeg",
        "video/quicktime",
        "video/webm",
        "video/x-msvideo",
    },
    "audio": {
        "audio/mpeg",
        "audio/wav",
        "audio/x-wav",
        "audio/mp4",
        "audio/ogg",
        "audio/webm",
    },
    "image": {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    },
}


def get_file_type(content_type: str | None) -> str:
    if not content_type:
        return "other"

    for file_type, mime_types in ALLOWED_FILE_TYPES.items():
        if content_type in mime_types:
            return file_type

    return "other"


@router.post(
    "/upload/{project_id}",
    response_model=MediaFileResponse,
)
async def upload_media(
    project_id: int,
    file: UploadFile = File(...),
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

    media_type = get_file_type(file.content_type)

    if media_type == "other":
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type",
        )

    os.makedirs(STORAGE_DIR, exist_ok=True)

    original_extension = os.path.splitext(
        file.filename or ""
    )[1]

    stored_filename = (
        f"{uuid.uuid4().hex}{original_extension}"
    )

    file_path = os.path.join(
        STORAGE_DIR,
        stored_filename,
    )

    max_size = settings.max_upload_size_mb * 1024 * 1024
    total_size = 0

    try:
        with open(file_path, "wb") as output_file:
            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > max_size:
                    output_file.close()

                    if os.path.exists(file_path):
                        os.remove(file_path)

                    raise HTTPException(
                        status_code=413,
                        detail=(
                            f"File is too large. "
                            f"Maximum size is "
                            f"{settings.max_upload_size_mb} MB."
                        ),
                    )

                output_file.write(chunk)

    finally:
        await file.close()

    media = MediaFile(
        project_id=project_id,
        filename=file.filename or stored_filename,
        file_type=media_type,
        file_path=file_path,
    )

    db.add(media)
    db.commit()
    db.refresh(media)

    return media


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
