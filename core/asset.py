from datetime import datetime, timezone
from typing import Any, Dict, Optional


ASSET_PREFIXES = {
    "character": "CHAR",
    "location": "LOC",
    "prop": "PROP",
    "vehicle": "VEH",
    "voice": "VOICE",
    "audio": "AUD",
    "video": "VID",
    "image": "IMG",
    "music": "MUS",
    "document": "DOC",
    "scene": "SCENE",
    "shot": "SHOT",
    "other": "ASSET",
}


class Asset:
    def __init__(
        self,
        asset_id: str,
        asset_type: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.id = asset_id
        self.type = asset_type
        self.name = name
        self.metadata = metadata or {}

        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at

        self.version = 1
        self.locked = False
        self.tags: list[str] = []

    def update(self, **fields: Any) -> None:
        for key, value in fields.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.version += 1
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
            "locked": self.locked,
            "tags": self.tags,
        }


class AssetManager:
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.counters: Dict[str, int] = {}

    def _generate_id(self, asset_type: str) -> str:
        prefix = ASSET_PREFIXES.get(asset_type, "ASSET")

        self.counters[prefix] = self.counters.get(prefix, 0) + 1

        return f"{prefix}-{self.counters[prefix]:03d}"

    def create_asset(
        self,
        asset_type: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Asset:
        asset_id = self._generate_id(asset_type)

        asset = Asset(
            asset_id=asset_id,
            asset_type=asset_type,
            name=name,
            metadata=metadata,
        )

        self.assets[asset_id] = asset

        return asset

    def get_asset(self, asset_id: str) -> Optional[Asset]:
        return self.assets.get(asset_id)

    def delete_asset(self, asset_id: str) -> bool:
        asset = self.assets.get(asset_id)

        if asset is None:
            return False

        if asset.locked:
            return False

        del self.assets[asset_id]
        return True

    def list_assets(
        self,
        asset_type: Optional[str] = None,
    ) -> list[Dict[str, Any]]:
        assets = self.assets.values()

        if asset_type:
            assets = [
                asset
                for asset in assets
                if asset.type == asset_type
            ]

        return [
            asset.snapshot()
            for asset in assets
        ]


asset_manager = AssetManager()
