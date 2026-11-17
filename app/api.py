from fastapi import APIRouter

from app.media_api import (
    router as media_router,
)

from app.project_api import (
    router as project_router,
)

from i18n.api import (
    router as i18n_router,
)

from seo.api import (
    router as seo_router,
)


router = APIRouter()


@router.get("/api/status")
def status():

    return {
        "status": "ok",
        "application": "ACOS",
        "message": "ACOS API is working",
    }


router.include_router(
    project_router
)

router.include_router(
    media_router
)

router.include_router(
    i18n_router
)

router.include_router(
    seo_router
)
