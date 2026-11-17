from dataclasses import dataclass
from typing import Callable


@dataclass
class LinguisticCheck:
    name: str
    score: float
    passed: bool
    details: str = ""


@dataclass
class LinguisticResult:
    language: str
    key: str
    source_text: str
    translated_text: str
    checks: list[LinguisticCheck]
    confidence: float
    status: str


class LinguisticValidator:

    def __init__(self):
        self.checkers: list[
            Callable[[str, str, str], LinguisticCheck]
        ] = []

    def register_checker(
        self,
        checker: Callable[
            [str, str, str],
            LinguisticCheck,
        ],
    ) -> None:
        self.checkers.append(checker)

    def validate(
        self,
        language: str,
        key: str,
        source_text: str,
        translated_text: str,
    ) -> LinguisticResult:

        checks = []

        for checker in self.checkers:
            result = checker(
                language,
                source_text,
                translated_text,
            )
            checks.append(result)

        if not checks:
            confidence = 0.0
        else:
            confidence = (
                sum(
                    check.score
                    for check in checks
                )
                / len(checks)
            )

        if confidence >= 95:
            status = "PASS"
        elif confidence >= 85:
            status = "REVIEW"
        elif confidence >= 70:
            status = "WARNING"
        else:
            status = "FAIL"

        return LinguisticResult(
            language=language,
            key=key,
            source_text=source_text,
            translated_text=translated_text,
            checks=checks,
            confidence=round(
                confidence,
                2,
            ),
            status=status,
        )


linguistic_validator = LinguisticValidator()
