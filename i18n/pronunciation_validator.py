from dataclasses import dataclass


@dataclass
class PronunciationCheck:
    engine: str
    score: float
    passed: bool
    details: str = ""


@dataclass
class PronunciationResult:
    language: str
    text: str
    checks: list[PronunciationCheck]
    confidence: float
    status: str


class PronunciationValidator:

    def __init__(self):
        self.engines = []

    def register_engine(self, engine):
        self.engines.append(engine)

    def validate(
        self,
        language: str,
        text: str,
        audio_path: str | None = None,
    ) -> PronunciationResult:

        checks = []

        for engine in self.engines:
            result = engine.check(
                language=language,
                text=text,
                audio_path=audio_path,
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

        return PronunciationResult(
            language=language,
            text=text,
            checks=checks,
            confidence=round(
                confidence,
                2,
            ),
            status=status,
        )


pronunciation_validator = PronunciationValidator()
