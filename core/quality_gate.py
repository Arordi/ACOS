from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class QualityCheck:
    name: str
    passed: bool
    score: float = 0.0
    message: str = ""


@dataclass
class QualityGateResult:
    operation_id: str

    passed: bool = False
    score: float = 0.0

    checks: List[QualityCheck] = field(default_factory=list)
    blocking_issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "passed": self.passed,
            "score": self.score,
            "checks": [
                {
                    "name": check.name,
                    "passed": check.passed,
                    "score": check.score,
                    "message": check.message,
                }
                for check in self.checks
            ],
            "blocking_issues": self.blocking_issues,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }


class QualityGate:
    """
    Final quality control for ACOS operations.

    An operation can only pass when all blocking checks pass.
    """

    def __init__(
        self,
        minimum_score: float = 0.80,
    ):
        self.minimum_score = minimum_score
        self.results: Dict[str, QualityGateResult] = {}

    def evaluate(
        self,
        operation_id: str,
        checks: List[QualityCheck],
    ) -> QualityGateResult:

        result = QualityGateResult(
            operation_id=operation_id,
            checks=checks,
        )

        if checks:
            result.score = sum(
                check.score for check in checks
            ) / len(checks)

        for check in checks:

            if not check.passed:
                result.blocking_issues.append(
                    f"{check.name}: {check.message}"
                )

        result.passed = (
            result.score >= self.minimum_score
            and not result.blocking_issues
        )

        self.results[operation_id] = result

        return result

    def add_check(
        self,
        operation_id: str,
        name: str,
        passed: bool,
        score: float,
        message: str = "",
    ) -> QualityGateResult:

        existing = self.results.get(operation_id)

        if existing:
            checks = existing.checks
        else:
            checks = []

        checks.append(
            QualityCheck(
                name=name,
                passed=passed,
                score=score,
                message=message,
            )
        )

        return self.evaluate(
            operation_id=operation_id,
            checks=checks,
        )

    def get_result(
        self,
        operation_id: str,
    ) -> QualityGateResult | None:

        return self.results.get(operation_id)


quality_gate = QualityGate()
