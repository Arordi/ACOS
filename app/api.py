from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from core.architect import architect
from core.project import project_manager
from core.asset import asset_manager


router = APIRouter(prefix="/api")


class ProjectCreateRequest(BaseModel):
    name: str


class ArchitectRequest(BaseModel):
    request: str
    context: Dict[str, Any] = {}


class AssetCreateRequest(BaseModel):
    asset_type: str
    name: str
    metadata: Dict[str, Any] = {}


@router.get("/status")
def status():
    return {
        "status": "ok",
        "system": "ACOS",
        "version": "0.1.0",
    }


@router.post("/projects")
def create_project(data: ProjectCreateRequest):
    project = project_manager.create_project(data.name)

    return {
        "success": True,
        "project": project.snapshot(),
    }


@router.get("/projects")
def list_projects():
    return {
        "success": True,
        "projects": project_manager.list_projects(),
    }


@router.post("/architect/analyze")
def analyze_request(data: ArchitectRequest):
    plan = architect.analyze(
        user_request=data.request,
        context=data.context,
    )

    return {
        "success": True,
        "plan": plan.snapshot(),
    }


@router.post("/assets")
def create_asset(data: AssetCreateRequest):
    asset = asset_manager.create_asset(
        asset_type=data.asset_type,
        name=data.name,
        metadata=data.metadata,
    )

    return {
        "success": True,
        "asset": asset.snapshot(),
    }


@router.get("/assets")
def list_assets():
    return {
        "success": True,
        "assets": asset_manager.list_assets(),
    }
