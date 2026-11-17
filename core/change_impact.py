from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ChangeImpact:
    """
    Describes the possible impact of a requested change.
    """

    operation_id: str

    affected_assets: List[str] = field(default_factory=list)
    affected_scenes: List[str] = field(default_factory=list)
    affected_shots: List[str] = field(default_factory=list)
    affected_tracks: List[str] = field(default_factory=list)
    affected_regions: List[str] = field(default_factory=list)

    requires_audio_rebuild: bool = False
    requires_video_rebuild: bool = False
    requires_lipsync: bool = False
    requires_translation: bool = False
    requires_render: bool = False

    risk_level: str = "low"

    warnings: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "affected_assets": self.affected_assets,
            "affected_scenes": self.affected_scenes,
            "affected_shots": self.affected_shots,
            "affected_tracks": self.affected_tracks,
            "affected_regions": self.affected_regions,
            "requires_audio_rebuild": self.requires_audio_rebuild,
            "requires_video_rebuild": self.requires_video_rebuild,
            "requires_lipsync": self.requires_lipsync,
            "requires_translation": self.requires_translation,
            "requires_render": self.requires_render,
            "risk_level": self.risk_level,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }


class ChangeImpactEngine:
    """
    Calculates the potential impact of a requested operation.
    """

    def __init__(self):
        self.impacts: Dict[str, ChangeImpact] = {}

    def create_impact(
        self,
        operation_id: str,
    ) -> ChangeImpact:

        impact = ChangeImpact(
            operation_id=operation_id,
        )

        self.impacts[operation_id] = impact

        return impact

    def get_impact(
        self,
        operation_id: str,
    ) -> ChangeImpact | None:

        return self.impacts.get(operation_id)

    def add_asset(
        self,
        operation_id: str,
        asset_id: str,
    ) -> None:

        impact = self.get_impact(operation_id)

        if not impact:
            impact = self.create_impact(operation_id)

        if asset_id not in impact.affected_assets:
            impact.affected_assets.append(asset_id)

    def add_scene(
        self,
        operation_id: str,
        scene_id: str,
    ) -> None:

        impact = self.get_impact(operation_id)

        if not impact:
            impact = self.create_impact(operation_id)

        if scene_id not in impact.affected_scenes:
            impact.affected_scenes.append(scene_id)

    def add_shot(
        self,
        operation_id: str,
        shot_id: str,
    ) -> None:

        impact = self.get_impact(operation_id)

        if not impact:
            impact = self.create_impact(operation_id)

        if shot_id not in impact.affected_shots:
            impact.affected_shots.append(shot_id)

    def add_track(
        self,
        operation_id: str,
        track_id: str,
    ) -> None:

        impact = self.get_impact(operation_id)

        if not impact:
            impact = self.create_impact(operation_id)

        if track_id not in impact.affected_tracks:
            impact.affected_tracks.append(track_id)

    def add_region(
        self,
        operation_id: str,
        region_id: str,
    ) -> None:

        impact = self.get_impact(operation_id)

        if not impact:
            impact = self.create_impact(operation_id)

        if region_id not in impact.affected_regions:
            impact.affected_regions.append(region_id)

    def set_requirements(
        self,
        operation_id: str,
        **requirements: bool,
    ) -> None:

        impact = self.get_impact(operation_id)

        if not impact:
            impact = self.create_impact(operation_id)

        for key, value in requirements.items():
            if hasattr(impact, key):
                setattr(impact, key, value)

    def add_warning(
        self,
        operation_id: str,
        warning: str,
    ) -> None:

        impact = self.get_impact(operation_id)

        if not impact:
            impact = self.create_impact(operation_id)

        if warning not in impact.warnings:
            impact.warnings.append(warning)

    def set_risk(
        self,
        operation_id: str,
        risk_level: str,
    ) -> None:

        impact = self.get_impact(operation_id)

        if not impact:
            impact = self.create_impact(operation_id)

        impact.risk_level = risk_level


change_impact_engine = ChangeImpactEngine()
