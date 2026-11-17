from dataclasses import dataclass


@dataclass
class QualityResult:
    structural_score: float
    linguistic_score: float
    dictionary_score: float
    pronunciation_score: float
    final_score: float
    status: str


class QualityEngine:

    def calculate(
        self,
        structural_score: float,
        linguistic_score: float,
        dictionary_score: float,
        pronunciation_score: float,
    ) -> QualityResult:

        scores = [
            structural_score,
            linguistic_score,
            dictionary_score,
            pronunciation_score,
        ]

        final_score = sum(scores) / len(scores)

        if final_score >= 95:
            status = "PASS"
        elif final_score >= 85:
            status = "REVIEW"
        elif final_score >= 70:
            status = "WARNING"
        else:
            status = "FAIL"

        return QualityResult(
            structural_score=structural_score,
            linguistic_score=linguistic_score,
            dictionary_score=dictionary_score,
            pronunciation_score=pronunciation_score,
            final_score=round(
                final_score,
                2,
            ),
            status=status,
        )


quality_engine = QualityEngine()
