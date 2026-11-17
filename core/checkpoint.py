from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class Checkpoint:
    checkpoint_id: str
    job_id: str

    step: str
    progress: float = 0.0

    state: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    def snapshot(self) -> Dict[str, Any]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "job_id": self.job_id,
            "step": self.step,
            "progress": self.progress,
            "state": self.state,
            "created_at": self.created_at,
        }


class CheckpointManager:
    def __init__(self):
        self.checkpoints: Dict[str, Checkpoint] = {}

    def save(
        self,
        checkpoint_id: str,
        job_id: str,
        step: str,
        progress: float,
        state: Optional[Dict[str, Any]] = None,
    ) -> Checkpoint:

        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            job_id=job_id,
            step=step,
            progress=progress,
            state=state or {},
        )

        self.checkpoints[checkpoint_id] = checkpoint

        return checkpoint

    def get(
        self,
        checkpoint_id: str,
    ) -> Optional[Checkpoint]:

        return self.checkpoints.get(checkpoint_id)

    def latest_for_job(
        self,
        job_id: str,
    ) -> Optional[Checkpoint]:

        matches = [
            checkpoint
            for checkpoint in self.checkpoints.values()
            if checkpoint.job_id == job_id
        ]

        if not matches:
            return None

        return max(
            matches,
            key=lambda item: item.created_at,
        )


@dataclass
class CacheEntry:
    cache_key: str
    value: Any

    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )


class CacheManager:
    def __init__(self):
        self.cache: Dict[str, CacheEntry] = {}

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.cache[key] = CacheEntry(
            cache_key=key,
            value=value,
        )

    def get(
        self,
        key: str,
    ) -> Any:

        entry = self.cache.get(key)

        if not entry:
            return None

        return entry.value

    def exists(
        self,
        key: str,
    ) -> bool:

        return key in self.cache

    def delete(
        self,
        key: str,
    ) -> bool:

        if key not in self.cache:
            return False

        del self.cache[key]
        return True


checkpoint_manager = CheckpointManager()
cache_manager = CacheManager()
