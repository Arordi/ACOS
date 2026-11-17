from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Region:
    """
    A specific editable or protected area of an asset/frame.
    """

    region_id: str
    asset_id: str

    region_type: str = "polygon"

    data: Dict[str, Any] = field(default_factory=dict)

    editable: bool = True
    protected: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    def lock(self) -> None:
        self.protected = True
        self.editable = False

    def unlock(self) -> None:
        self.protected = False
        self.editable = True

    def snapshot(self) -> Dict[str, Any]:
        return {
            "region_id": self.region_id,
            "asset_id": self.asset_id,
            "region_type": self.region_type,
            "data": self.data,
            "editable": self.editable,
            "protected": self.protected,
            "metadata": self.metadata,
        }


class MaskEngine:
    """
    Manages editable and protected regions.

    Later this can be connected to:
    - segmentation models
    - object detection
    - video tracking
    - SAM-style segmentation
    - face/body/object masks
    """

    def __init__(self):
        self.regions: Dict[str, Region] = {}

    def create_region(
        self,
        region_id: str,
        asset_id: str,
        region_type: str = "polygon",
        data: Optional[Dict[str, Any]] = None,
    ) -> Region:

        region = Region(
            region_id=region_id,
            asset_id=asset_id,
            region_type=region_type,
            data=data or {},
        )

        self.regions[region_id] = region

        return region

    def get_region(
        self,
        region_id: str,
    ) -> Optional[Region]:

        return self.regions.get(region_id)

    def lock_region(
        self,
        region_id: str,
    ) -> bool:

        region = self.get_region(region_id)

        if not region:
            return False

        region.lock()

        return True

    def unlock_region(
        self,
        region_id: str,
    ) -> bool:

        region = self.get_region(region_id)

        if not region:
            return False

        region.unlock()

        return True

    def can_edit(
        self,
        region_id: str,
    ) -> bool:

        region = self.get_region(region_id)

        if not region:
            return False

        return region.editable and not region.protected

    def list_asset_regions(
        self,
        asset_id: str,
    ) -> List[Dict[str, Any]]:

        return [
            region.snapshot()
            for region in self.regions.values()
            if region.asset_id == asset_id
        ]


mask_engine = MaskEngine()
