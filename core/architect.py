from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class ArchitectPlan:
    plan_id: str

    user_request: str

    intent: str = ""
    scope: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)

    steps: List[Dict[str, Any]] = field(default_factory=list)

    recommended_tools: List[str] = field(default_factory=list)
    recommended_models: List[str] = field(default_factory=list)

    estimated_cost: Optional[float] = None
    risk_level: str = "low"

    requires_approval: bool = True

    status: str = "draft"

    metadata: Dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "user_request": self.user_request,
            "intent": self.intent,
            "scope": self.scope,
            "constraints": self.constraints,
            "steps": self.steps,
            "recommended_tools": self.recommended_tools,
            "recommended_models": self.recommended_models,
            "estimated_cost": self.estimated_cost,
            "risk_level": self.risk_level,
            "requires_approval": self.requires_approval,
            "status": self.status,
            "metadata": self.metadata,
        }


class AIProductArchitect:
    """
    ACOS planning layer.

    The Architect analyzes a request and creates a plan.
    It does not execute changes by itself.
    """

    def __init__(self):
        self.plans: Dict[str, ArchitectPlan] = {}

    def analyze(
        self,
        user_request: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> ArchitectPlan:

        plan = ArchitectPlan(
            plan_id=f"PLAN-{uuid4().hex[:12].upper()}",
            user_request=user_request,
        )

        plan.intent = self._detect_intent(user_request)

        plan.scope = {
            "context": context or {},
            "source": "user_request",
        }

        plan.constraints = {
            "human_approval_required": True,
            "preserve_unrequested_content": True,
            "non_destructive": True,
        }

        plan.steps = [
            {
                "step": 1,
                "action": "understand_request",
                "status": "planned",
            },
            {
                "step": 2,
                "action": "define_scope",
                "status": "planned",
            },
            {
                "step": 3,
                "action": "select_tools_and_models",
                "status": "planned",
            },
            {
                "step": 4,
                "action": "estimate_cost_and_risk",
                "status": "planned",
            },
            {
                "step": 5,
                "action": "request_user_approval",
                "status": "planned",
            },
            {
                "step": 6,
                "action": "execute_after_approval",
                "status": "blocked_until_approval",
            },
            {
                "step": 7,
                "action": "run_quality_gate",
                "status": "planned",
            },
        ]

        plan.status = "awaiting_approval"

        self.plans[plan.plan_id] = plan

        return plan

    def _detect_intent(
        self,
        request: str,
    ) -> str:

        text = request.lower()

        if any(
            word in text
            for word in [
                "translate",
                "translation",
                "թարգման",
                "перевод",
            ]
        ):
            return "translation"

        if any(
            word in text
            for word in [
                "edit",
                "change",
                "modify",
                "փոխիր",
                "փոփոխիր",
            ]
        ):
            return "precision_edit"

        if any(
            word in text
            for word in [
                "generate",
                "create",
                "ստեղծիր",
                "ստեղծել",
            ]
        ):
            return "generation"

        if any(
            word in text
            for word in [
                "analyze",
                "analysis",
                "վերլուծ",
            ]
        ):
            return "analysis"

        return "general_creative_task"

    def approve(
        self,
        plan_id: str,
    ) -> bool:

        plan = self.plans.get(plan_id)

        if not plan:
            return False

        plan.status = "approved"

        return True

    def reject(
        self,
        plan_id: str,
    ) -> bool:

        plan = self.plans.get(plan_id)

        if not plan:
            return False

        plan.status = "rejected"

        return True

    def get_plan(
        self,
        plan_id: str,
    ) -> Optional[ArchitectPlan]:

        return self.plans.get(plan_id)


architect = AIProductArchitect()
