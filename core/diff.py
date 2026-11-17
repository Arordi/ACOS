from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DiffResult:
    operation_id: str

    changed: bool = False
    approved: bool = False

    changed_fields: List[str] = field(default_factory=list)
    unexpected_changes: List[str] = field(default_factory=list)
    protected_changes: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "changed": self.changed,
            "approved": self.approved,
            "changed_fields": self.changed_fields,
            "unexpected_changes": self.unexpected_changes,
            "protected_changes": self.protected_changes,
            "warnings": self.warnings,
            "metadata": self.metadata,
        }


class OutputDiffEngine:
    """
    Compares the original state with the new state.

    Used by ACOS to detect:
    - requested changes
    - unexpected changes
    - protected changes
    """

    def __init__(self):
        self.results: Dict[str, DiffResult] = {}

    def compare(
        self,
        operation_id: str,
        original: Dict[str, Any],
        updated: Dict[str, Any],
        allowed_fields: List[str] | None = None,
        protected_fields: List[str] | None = None,
    ) -> DiffResult:

        result = DiffResult(
            operation_id=operation_id,
        )

        allowed = set(allowed_fields or [])
        protected = set(protected_fields or [])

        all_keys = set(original.keys()) | set(updated.keys())

        for key in sorted(all_keys):

            old_value = original.get(key)
            new_value = updated.get(key)

            if old_value == new_value:
                continue

            result.changed = True
            result.changed_fields.append(key)

            if key in protected:
                result.protected_changes.append(key)

            elif allowed and key not in allowed:
                result.unexpected_changes.append(key)

        if result.protected_changes:
            result.approved = False

            result.warnings.append(
                "Protected content was changed."
            )

        elif result.unexpected_changes:
            result.approved = False

            result.warnings.append(
                "Unexpected changes were detected."
            )

        else:
            result.approved = True

        self.results[operation_id] = result

        return result

    def get_result(
        self,
        operation_id: str,
    ) -> DiffResult | None:

        return self.results.get(operation_id)


diff_engine = OutputDiffEngine()
