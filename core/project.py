from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4

from core.context import ProjectContext


class Project:
    def __init__(
        self,
        name: str,
        project_id: Optional[str] = None,
    ):
        self.id = project_id or f"PROJ-{uuid4().hex[:12].upper()}"
        self.name = name
        self.status = "active"
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at

        self.context = ProjectContext(project_id=self.id)

        self.assets: Dict[str, Dict[str, Any]] = {}
        self.scenes: Dict[str, Dict[str, Any]] = {}
        self.shots: Dict[str, Dict[str, Any]] = {}

    def update(self, **fields: Any) -> None:
        for key, value in fields.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_asset(
        self,
        asset_id: str,
        asset_type: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.assets[asset_id] = {
            "id": asset_id,
            "type": asset_type,
            "name": name,
            "metadata": metadata or {},
        }

    def add_scene(
        self,
        scene_id: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.scenes[scene_id] = {
            "id": scene_id,
            "name": name,
            "metadata": metadata or {},
        }

    def add_shot(
        self,
        shot_id: str,
        scene_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.shots[shot_id] = {
            "id": shot_id,
            "scene_id": scene_id,
            "metadata": metadata or {},
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "assets": self.assets,
            "scenes": self.scenes,
            "shots": self.shots,
            "context": self.context.snapshot(),
        }


class ProjectManager:
    def __init__(self):
        self.projects: Dict[str, Project] = {}

    def create_project(self, name: str) -> Project:
        project = Project(name=name)
        self.projects[project.id] = project
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def delete_project(self, project_id: str) -> bool:
        if project_id not in self.projects:
            return False

        del self.projects[project_id]
        return True

    def list_projects(self) -> list[Dict[str, Any]]:
        return [
            {
                "id": project.id,
                "name": project.name,
                "status": project.status,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
            for project in self.projects.values()
        ]


project_manager = ProjectManager()
