from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import uuid4


@dataclass
class ApprovalRequest:
    approval_id: str
    operation_id: str

    title: str
    description: str

    risk_level: str = "low"
    estimated_cost: Optional[float] = None

    requires_confirmation: bool = True
    confirmed: bool = False
    rejected: bool = False

    created_at: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    metadata: Dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "operation_id": self.operation_id,
            "title": self.title,
            "description": self.description,
            "risk_level": self.risk_level,
            "estimated_cost": self.estimated_cost,
            "requires_confirmation": self.requires_confirmation,
            "confirmed": self.confirmed,
            "rejected": self.rejected,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


class ApprovalEngine:
    """
    Human approval layer for ACOS.

    Operations remain blocked until explicitly approved.
    """

    def __init__(self):
        self.requests: Dict[str, ApprovalRequest] = {}

    def create_request(
        self,
        operation_id: str,
        title: str,
        description: str,
        risk_level: str = "low",
        estimated_cost: Optional[float] = None,
    ) -> ApprovalRequest:

        approval = ApprovalRequest(
            approval_id=f"APR-{uuid4().hex[:12].upper()}",
            operation_id=operation_id,
            title=title,
            description=description,
            risk_level=risk_level,
            estimated_cost=estimated_cost,
        )

        self.requests[approval.approval_id] = approval

        return approval

    def confirm(
        self,
        approval_id: str,
    ) -> bool:

        approval = self.requests.get(approval_id)

        if not approval or approval.rejected:
            return False

        approval.confirmed = True

        return True

    def reject(
        self,
        approval_id: str,
    ) -> bool:

        approval = self.requests.get(approval_id)

        if not approval or approval.confirmed:
            return False

        approval.rejected = True

        return True

    def is_approved(
        self,
        approval_id: str,
    ) -> bool:

        approval = self.requests.get(approval_id)

        if not approval:
            return False

        return approval.confirmed and not approval.rejected

    def get(
        self,
        approval_id: str,
    ) -> Optional[ApprovalRequest]:

        return self.requests.get(approval_id)


approval_engine = ApprovalEngine()
