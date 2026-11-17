from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class AuditEvent:
    event_id: str
    event_type: str

    user_id: Optional[str] = None
    project_id: Optional[str] = None
    operation_id: Optional[str] = None
    job_id: Optional[str] = None

    action: str = ""

    provider: Optional[str] = None
    model: Optional[str] = None
    tool: Optional[str] = None

    input_hash: Optional[str] = None
    output_hash: Optional[str] = None

    status: str = "recorded"

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    def snapshot(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "operation_id": self.operation_id,
            "job_id": self.job_id,
            "action": self.action,
            "provider": self.provider,
            "model": self.model,
            "tool": self.tool,
            "input_hash": self.input_hash,
            "output_hash": self.output_hash,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


class AuditEngine:
    """
    Records important ACOS actions for traceability,
    debugging, reproducibility and security.
    """

    def __init__(self):
        self.events: List[AuditEvent] = []

    def record(
        self,
        event_type: str,
        action: str,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        operation_id: Optional[str] = None,
        job_id: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        tool: Optional[str] = None,
        input_hash: Optional[str] = None,
        output_hash: Optional[str] = None,
        status: str = "recorded",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEvent:

        event = AuditEvent(
            event_id=f"AUD-{uuid4().hex[:12].upper()}",
            event_type=event_type,
            action=action,
            user_id=user_id,
            project_id=project_id,
            operation_id=operation_id,
            job_id=job_id,
            provider=provider,
            model=model,
            tool=tool,
            input_hash=input_hash,
            output_hash=output_hash,
            status=status,
            metadata=metadata or {},
        )

        self.events.append(event)

        return event

    def list_events(
        self,
        project_id: Optional[str] = None,
        operation_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:

        events = self.events

        if project_id:
            events = [
                event
                for event in events
                if event.project_id == project_id
            ]

        if operation_id:
            events = [
                event
                for event in events
                if event.operation_id == operation_id
            ]

        return [
            event.snapshot()
            for event in events
        ]


audit_engine = AuditEngine()
