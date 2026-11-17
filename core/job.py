from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass
class Job:
    job_id: str
    operation_id: str
    job_type: str

    status: str = "queued"
    progress: float = 0.0

    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)

    error: Optional[str] = None

    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    def update_status(
        self,
        status: str,
        progress: Optional[float] = None,
    ) -> None:

        self.status = status

        if progress is not None:
            self.progress = max(
                0.0,
                min(100.0, progress),
            )

        self.updated_at = datetime.now(
            timezone.utc
        ).isoformat()

    def fail(self, error: str) -> None:
        self.status = "failed"
        self.error = error
        self.updated_at = datetime.now(
            timezone.utc
        ).isoformat()

    def complete(
        self,
        output_data: Optional[Dict[str, Any]] = None,
    ) -> None:

        self.status = "completed"
        self.progress = 100.0

        if output_data:
            self.output_data = output_data

        self.updated_at = datetime.now(
            timezone.utc
        ).isoformat()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "operation_id": self.operation_id,
            "job_type": self.job_type,
            "status": self.status,
            "progress": self.progress,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "error": self.error,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class JobManager:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}

    def create_job(
        self,
        operation_id: str,
        job_type: str,
        input_data: Optional[Dict[str, Any]] = None,
    ) -> Job:

        job = Job(
            job_id=f"JOB-{uuid4().hex[:12].upper()}",
            operation_id=operation_id,
            job_type=job_type,
            input_data=input_data or {},
        )

        self.jobs[job.job_id] = job

        return job

    def get_job(
        self,
        job_id: str,
    ) -> Optional[Job]:

        return self.jobs.get(job_id)

    def start_job(
        self,
        job_id: str,
    ) -> bool:

        job = self.get_job(job_id)

        if not job:
            return False

        job.update_status(
            status="running",
            progress=0.0,
        )

        return True

    def complete_job(
        self,
        job_id: str,
        output_data: Optional[Dict[str, Any]] = None,
    ) -> bool:

        job = self.get_job(job_id)

        if not job:
            return False

        job.complete(output_data)

        return True

    def fail_job(
        self,
        job_id: str,
        error: str,
    ) -> bool:

        job = self.get_job(job_id)

        if not job:
            return False

        job.fail(error)

        return True


job_manager = JobManager()
