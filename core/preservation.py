from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class PreservationPolicy:
    """
    Defines what ACOS must preserve during an operation.
    """

    preserve_audio: bool = True
    preserve_video: bool = True
    preserve_dialogue: bool = True
    preserve_music: bool = True
    preserve_sfx: bool = True
    preserve_timing: bool = True
    preserve_camera: bool = True
    preserve_lighting: bool = True
    preserve_style: bool = True
    preserve_character_identity: bool = True
    preserve_location: bool = True
    preserve_background: bool = True

    protected_objects: set[str] = field(default_factory=set)
    protected_regions: set[str] = field(default_factory=set)
    protected_tracks: set[str] = field(default_factory=set)

    custom_rules: Dict[str, Any] = field(default_factory=dict)


class PreservationEngine:
    """
    Checks whether an operation is allowed to modify
    protected content.
    """

    def __init__(self):
        self.policies: Dict[str, PreservationPolicy] = {}

    def create_policy(
        self,
        operation_id: str,
        **kwargs: Any,
    ) -> PreservationPolicy:

        policy = PreservationPolicy(**kwargs)
        self.policies[operation_id] = policy

        return policy

    def get_policy(
        self,
        operation_id: str,
    ) -> PreservationPolicy | None:

        return self.policies.get(operation_id)

    def protect_object(
        self,
        operation_id: str,
        object_id: str,
    ) -> bool:

        policy = self.get_policy(operation_id)

        if not policy:
            return False

        policy.protected_objects.add(object_id)
        return True

    def protect_region(
        self,
        operation_id: str,
        region_id: str,
    ) -> bool:

        policy = self.get_policy(operation_id)

        if not policy:
            return False

        policy.protected_regions.add(region_id)
        return True

    def protect_track(
        self,
        operation_id: str,
        track_id: str,
    ) -> bool:

        policy = self.get_policy(operation_id)

        if not policy:
            return False

        policy.protected_tracks.add(track_id)
        return True

    def is_protected(
        self,
        operation_id: str,
        object_id: str | None = None,
        region_id: str | None = None,
        track_id: str | None = None,
    ) -> bool:

        policy = self.get_policy(operation_id)

        if not policy:
            return False

        if object_id and object_id in policy.protected_objects:
            return True

        if region_id and region_id in policy.protected_regions:
            return True

        if track_id and track_id in policy.protected_tracks:
            return True

        return False

    def check_change(
        self,
        operation_id: str,
        object_id: str | None = None,
        region_id: str | None = None,
        track_id: str | None = None,
    ) -> tuple[bool, str]:

        if self.is_protected(
            operation_id=operation_id,
            object_id=object_id,
            region_id=region_id,
            track_id=track_id,
        ):
            return False, "The requested element is protected."

        return True, "Change is allowed."


preservation_engine = PreservationEngine()
