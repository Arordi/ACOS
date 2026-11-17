from fastapi import APIRouter

from app.project_api import router as project_router


router = APIRouter()


@router.get("/api/status")
def status():
    return {
        "status": "ok",
        "application": "ACOS",
        "message": "ACOS API is working",
    }


router.include_router(project_router)
