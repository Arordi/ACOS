from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class ProviderStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    UNSUPPORTED = "unsupported"
    DISABLED = "disabled"


@dataclass
class ProviderResult:
    provider: str
    status: ProviderStatus
    value: Any = None
    score: float = 0.0
    confidence: float = 0.0
    cost: float = 0.0
    latency_ms: float = 0.0
    details: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConsensusResult:
    value: Any
    confidence: float
    status: str
    providers_used: list[str]
    successful_providers: int
    failed_providers: int
    unsupported_providers: int
    disagreement: bool
    details: list[str] = field(default_factory=list)


class TranslationProvider(Protocol):

    name: str

    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> ProviderResult:
        ...


class DictionaryProvider(Protocol):

    name: str

    async def check(
        self,
        text: str,
        language: str,
    ) -> ProviderResult:
        ...


class GrammarProvider(Protocol):

    name: str

    async def check(
        self,
        text: str,
        language: str,
    ) -> ProviderResult:
        ...


class PronunciationProvider(Protocol):

    name: str

    async def check(
        self,
        text: str,
        language: str,
        audio_path: str | None = None,
    ) -> ProviderResult:
        ...


class ProviderRegistry:

    def __init__(self):
        self.translation_providers: list[TranslationProvider] = []
        self.dictionary_providers: list[DictionaryProvider] = []
        self.grammar_providers: list[GrammarProvider] = []
        self.pronunciation_providers: list[PronunciationProvider] = []

    def register_translation(self, provider: TranslationProvider):
        self.translation_providers.append(provider)

    def register_dictionary(self, provider: DictionaryProvider):
        self.dictionary_providers.append(provider)

    def register_grammar(self, provider: GrammarProvider):
        self.grammar_providers.append(provider)

    def register_pronunciation(self, provider: PronunciationProvider):
        self.pronunciation_providers.append(provider)


class QualityOrchestrator:

    def __init__(
        self,
        registry: ProviderRegistry,
        max_concurrency: int = 10,
    ):
        self.registry = registry
        self.max_concurrency = max_concurrency

    async def _run_provider(
        self,
        provider_call,
    ) -> ProviderResult:

        try:
            result = await provider_call()
            return result

        except Exception as exc:
            return ProviderResult(
                provider="unknown",
                status=ProviderStatus.FAILED,
                score=0.0,
                confidence=0.0,
                details=str(exc),
            )

    async def _run_many(
        self,
        calls,
    ) -> list[ProviderResult]:

        semaphore = asyncio.Semaphore(
            self.max_concurrency
        )

        async def limited_call(call):
            async with semaphore:
                return await self._run_provider(call)

        return await asyncio.gather(
            *[
                limited_call(call)
                for call in calls
            ]
        )

    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> ConsensusResult:

        calls = [
            lambda provider=provider: provider.translate(
                text=text,
                source_language=source_language,
                target_language=target_language,
            )
            for provider in self.registry.translation_providers
        ]

        results = await self._run_many(calls)

        return self._build_translation_consensus(
            results
        )

    async def check_dictionary(
        self,
        text: str,
        language: str,
    ) -> list[ProviderResult]:

        calls = [
            lambda provider=provider: provider.check(
                text=text,
                language=language,
            )
            for provider in self.registry.dictionary_providers
        ]

        return await self._run_many(calls)

    async def check_grammar(
        self,
        text: str,
        language: str,
    ) -> list[ProviderResult]:

        calls = [
            lambda provider=provider: provider.check(
                text=text,
                language=language,
            )
            for provider in self.registry.grammar_providers
        ]

        return await self._run_many(calls)

    async def check_pronunciation(
        self,
        text: str,
        language: str,
        audio_path: str | None = None,
    ) -> list[ProviderResult]:

        calls = [
            lambda provider=provider: provider.check(
                text=text,
                language=language,
                audio_path=audio_path,
            )
            for provider in self.registry.pronunciation_providers
        ]

        return await self._run_many(calls)

    def _build_translation_consensus(
        self,
        results: list[ProviderResult],
    ) -> ConsensusResult:

        successful = [
            result
            for result in results
            if result.status == ProviderStatus.SUCCESS
            and result.value is not None
        ]

        failed = [
            result
            for result in results
            if result.status == ProviderStatus.FAILED
        ]

        unsupported = [
            result
            for result in results
            if result.status == ProviderStatus.UNSUPPORTED
        ]

        if not successful:
            return ConsensusResult(
                value=None,
                confidence=0.0,
                status="FAIL",
                providers_used=[],
                successful_providers=0,
                failed_providers=len(failed),
                unsupported_providers=len(unsupported),
                disagreement=False,
                details=[
                    "No translation provider returned a usable result."
                ],
            )

        groups: dict[str, list[ProviderResult]] = {}

        for result in successful:
            normalized = self._normalize_text(
                str(result.value)
            )

            groups.setdefault(
                normalized,
                []
            ).append(result)

        ranked_groups = sorted(
            groups.items(),
            key=lambda item: (
                len(item[1]),
                sum(
                    provider.confidence
                    for provider in item[1]
                ),
            ),
            reverse=True,
        )

        best_value, best_results = ranked_groups[0]

        disagreement = len(groups) > 1

        confidence = self._calculate_confidence(
            best_results,
            len(successful),
            disagreement,
        )

        status = self._status_from_confidence(
            confidence
        )

        details = []

        if disagreement:
            details.append(
                "Translation providers disagree."
            )

            if len(ranked_groups) > 1:
                details.append(
                    "Conflicting translation candidates "
                    "were detected."
                )

        return ConsensusResult(
            value=best_results[0].value,
            confidence=confidence,
            status=status,
            providers_used=[
                result.provider
                for result in successful
            ],
            successful_providers=len(successful),
            failed_providers=len(failed),
            unsupported_providers=len(unsupported),
            disagreement=disagreement,
            details=details,
        )

    @staticmethod
    def _normalize_text(text: str) -> str:
        return " ".join(
            text.strip().lower().split()
        )

    @staticmethod
    def _calculate_confidence(
        best_results: list[ProviderResult],
        successful_count: int,
        disagreement: bool,
    ) -> float:

        provider_confidence = (
            sum(
                result.confidence
                for result in best_results
            )
            / len(best_results)
        )

        agreement_ratio = (
            len(best_results)
            / successful_count
        )

        confidence = (
            provider_confidence * 0.70
            + agreement_ratio * 100 * 0.30
        )

        if disagreement and agreement_ratio < 0.5:
            confidence -= 15

        return round(
            max(0.0, min(100.0, confidence)),
            2,
        )

    @staticmethod
    def _status_from_confidence(
        confidence: float,
    ) -> str:

        if confidence >= 95:
            return "PASS"

        if confidence >= 85:
            return "REVIEW"

        if confidence >= 70:
            return "WARNING"

        return "FAIL"


provider_registry = ProviderRegistry()

quality_orchestrator = QualityOrchestrator(
    registry=provider_registry
)
