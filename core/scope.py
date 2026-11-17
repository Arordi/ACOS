from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ScopeLock:
    """
    Defines exactly what ACOS is allowed to modify.

    Everything outside the declared scope is protected.
    """

    project_id: Optional[str] = None

    scene_ids: set[str] = field(default_factory=set)
    shot_ids: set[str] = field(default_factory=set)
    asset_ids: set[str] = field(default_factory=set)

    allowed_regions: Dict[str, Any] = field(default_factory=dict)
    allowed_tracks: set[str] = field(default_factory=set)

    locked_regions: Dict[str, Any] = field(default_factory=dict)
    locked_assets: set[str] = field(default_factory=set)

    preserve_audio: bool = True
    preserve_video: bool = True
    preserve_dialogue: bool = True
    preserve_music: bool = True
    preserve_timing: bool = True
    preserve_style: bool = True

    def allows_shot(self, shot_id: str) -> bool:
        if not self.shot_ids:
            return True

        return shot_id in self.shot_ids

    def allows_asset(self, asset_id: str) -> bool:
        if asset_id in self.locked_assets:
            return False

        if not self.asset_ids:
            return True

        return asset_id in self.asset_ids

    def allows_track(self, track_id: str) -> bool:
        if not self.allowed_tracks:
            return True

        return track_id in self.allowed_tracks

    def is_region_locked(
        self,
        asset_id: str,
        region_id: str,
    ) -> bool:
        locked = self.locked_regions.get(asset_id, set())

        return region_id in locked

    def validate_change(
        self,
        shot_id: Optional[str] = None,
        asset_id: Optional[str] = None,
        track_id: Optional[str] = None,
        region_id: Optional[str] = None,
    ) -> tuple[bool, str]:

        if shot_id and not self.allows_shot(shot_id):
            return False, "Shot is outside the allowed scope."

        if asset_id and not self.allows_asset(asset_id):
            return False, "Asset is outside the allowed scope or locked."

        if track_id and not self.allows_track(track_id):
            return False, "Track is outside the allowed scope."

        if asset_id and region_id:
            if self.is_region_locked(asset_id, region_id):
                return False, "Region is locked."

        return True, "Change is allowed."


class ScopeManager:
    def __init__(self):
        self.scopes: Dict[str, ScopeLock] = {}

    def create_scope(
        self,
        scope_id: str,
        project_id: Optional[str] = None,
    ) -> ScopeLock:

        scope = ScopeLock(project_id=project_id)
        self.scopes[scope_id] = scope

        return scope

    def get_scope(
        self,
        scope_id: str,
    ) -> Optional[ScopeLock]:

        return self.scopes.get(scope_id)

    def delete_scope(
        self,
        scope_id: str,
    ) -> bool:

        if scope_id not in self.scopes:
            return False

        del self.scopes[scope_id]
        return True


scope_manager = ScopeManager()
