from typing import Any, Dict, Optional


class ProjectContext:
    """
    ACOS project context.

    Keeps the active project, selected assets, current scene/shot,
    user instructions and protected constraints.
    """

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id
        self.active_scene_id: Optional[str] = None
        self.active_shot_id: Optional[str] = None

        self.selected_assets: list[str] = []
        self.locked_assets: list[str] = []

        self.user_instruction: Optional[str] = None

        self.constraints: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}

    def set_project(self, project_id: str) -> None:
        self.project_id = project_id

    def set_scene(self, scene_id: str) -> None:
        self.active_scene_id = scene_id

    def set_shot(self, shot_id: str) -> None:
        self.active_shot_id = shot_id

    def select_asset(self, asset_id: str) -> None:
        if asset_id not in self.selected_assets:
            self.selected_assets.append(asset_id)

    def lock_asset(self, asset_id: str) -> None:
        if asset_id not in self.locked_assets:
            self.locked_assets.append(asset_id)

    def set_instruction(self, instruction: str) -> None:
        self.user_instruction = instruction

    def add_constraint(self, key: str, value: Any) -> None:
        self.constraints[key] = value

    def snapshot(self) -> Dict[str, Any]:
        return {
            "project_id": self.project_id,
            "active_scene_id": self.active_scene_id,
            "active_shot_id": self.active_shot_id,
            "selected_assets": self.selected_assets,
            "locked_assets": self.locked_assets,
            "user_instruction": self.user_instruction,
            "constraints": self.constraints,
            "metadata": self.metadata,
        }
