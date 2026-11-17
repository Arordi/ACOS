from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol

from i18n.providers import (
    ProviderInfo,
    ProviderManager,
    provider_manager,
)


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

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


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

    details: list[str] = field(
        default_factory=list
    )


class TranslationProvider(Protocol):

    name: str

    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> Any:
        ...


class DictionaryProvider(Protocol):

    name: str

    async def check(
        self,
        text: str,
        language: str,
    ) -> Any:
        ...


class GrammarProvider(Protocol):

    name: str

    async def check(
        self,
        text: str,
        language: str,
    ) -> Any:
        ...


class PronunciationProvider(Protocol):

    name: str

    async def check(
        self,
        text: str,
        language: str,
    ) -> Any:
        ...


class ProviderRegistry:

    def __init__(
        self,
        manager: ProviderManager,
    ):
        self.manager = manager

        self.translation_providers: list[
            TranslationProvider
        ] = []

        self.dictionary_providers: list[
            DictionaryProvider
        ] = []

        self.grammar_providers: list[
            GrammarProvider
        ] = []

        self.pronunciation_providers: list[
            PronunciationProvider
        ] = []

    def register_translation(
        self,
        provider: TranslationProvider,
    ) -> None:

        if provider not in self.translation_providers:
            self.translation_providers.append(
                provider
            )

    def register_dictionary(
        self,
        provider: DictionaryProvider,
    ) -> None:

        if provider not in self.dictionary_providers:
            self.dictionary_providers.append(
                provider
            )

    def register_grammar(
        self,
        provider: GrammarProvider,
    ) -> None:

        if provider not in self.grammar_providers:
            self.grammar_providers.append(
                provider
            )

    def register_pronunciation(
        self,
        provider: PronunciationProvider,
    ) -> None:

        if provider not in self.pronunciation_providers:
            self.pronunciation_providers.append(
                provider
            )


class QualityOrchestrator:

    def __init__(
        self,
        registry: ProviderRegistry,
        max_concurrency: int = 10,
    ):

        self.registry = registry

        self.max_concurrency = max(
            1,
            max_concurrency,
        )

        self._semaphore = asyncio.Semaphore(
            self.max_concurrency
        )

    async def _run_provider(
        self,
        provider_name: str,
        callback,
    ) -> ProviderResult:

        loop = asyncio.get_running_loop()

        start_time = loop.time()

        try:

            async with self._semaphore:

                value = await callback()

            latency_ms = (
                loop.time() - start_time
            ) * 1000

            if isinstance(
                value,
                ProviderResult,
            ):

                if not value.provider:
                    value.provider = provider_name

                if value.latency_ms <= 0:
                    value.latency_ms = latency_ms

                return value

            return ProviderResult(
                provider=provider_name,
                status=ProviderStatus.SUCCESS,
                value=value,
                confidence=100.0,
                latency_ms=latency_ms,
            )

        except asyncio.CancelledError:

            raise

        except Exception as exc:

            latency_ms = (
                loop.time() - start_time
            ) * 1000

            return ProviderResult(
                provider=provider_name,
                status=ProviderStatus.FAILED,
                value=None,
                confidence=0.0,
                latency_ms=latency_ms,
                details=str(exc),
                metadata={
                    "exception_type": type(
                        exc
                    ).__name__,
                },
            )

    async def _run_many(
        self,
        calls: list[
            tuple[str, Any]
        ],
    ) -> list[ProviderResult]:

        if not calls:
            return []

        tasks = [
            self._run_provider(
                provider_name,
                callback,
            )
            for provider_name, callback
            in calls
        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=False,
        )

        return list(results)

    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> ConsensusResult:

        if not text or not text.strip():

            return ConsensusResult(
                value="",
                confidence=0.0,
                status="FAIL",
                providers_used=[],
                successful_providers=0,
                failed_providers=0,
                unsupported_providers=0,
                disagreement=False,
                details=[
                    "Input text is empty."
                ],
            )

        source_language = (
            source_language.strip().lower()
        )

        target_language = (
            target_language.strip().lower()
        )

        calls = []

        for provider in (
            self.registry.translation_providers
        ):

            provider_name = (
                self._get_provider_name(
                    provider
                )
            )

            if not provider_name:
                continue

            if not self._provider_available(
                provider,
                target_language,
                "translation",
            ):
                continue

            calls.append(
                (
                    provider_name,
                    lambda provider=provider:
                    provider.translate(
                        text=text,
                        source_language=source_language,
                        target_language=target_language,
                    ),
                )
            )

        results = await self._run_many(
            calls
        )

        return self._build_translation_consensus(
            results
        )

    async def check_dictionary(
        self,
        text: str,
        language: str,
    ) -> ConsensusResult:

        if not text or not text.strip():

            return ConsensusResult(
                value=None,
                confidence=0.0,
                status="FAIL",
                providers_used=[],
                successful_providers=0,
                failed_providers=0,
                unsupported_providers=0,
                disagreement=False,
                details=[
                    "Input text is empty."
                ],
            )

        language = language.strip().lower()

        calls = []

        for provider in (
            self.registry.dictionary_providers
        ):

            provider_name = (
                self._get_provider_name(
                    provider
                )
            )

            if not provider_name:
                continue

            if not self._provider_available(
                provider,
                language,
                "dictionary",
            ):
                continue

            calls.append(
                (
                    provider_name,
                    lambda provider=provider:
                    provider.check(
                        text=text,
                        language=language,
                    ),
                )
            )

        results = await self._run_many(
            calls
        )

        return self._build_generic_consensus(
            results,
            "dictionary",
        )

    async def check_grammar(
        self,
        text: str,
        language: str,
    ) -> ConsensusResult:

        if not text or not text.strip():

            return ConsensusResult(
                value=None,
                confidence=0.0,
                status="FAIL",
                providers_used=[],
                successful_providers=0,
                failed_providers=0,
                unsupported_providers=0,
                disagreement=False,
                details=[
                    "Input text is empty."
                ],
            )

        language = language.strip().lower()

        calls = []

        for provider in (
            self.registry.grammar_providers
        ):

            provider_name = (
                self._get_provider_name(
                    provider
                )
            )

            if not provider_name:
                continue

            if not self._provider_available(
                provider,
                language,
                "grammar",
            ):
                continue

            calls.append(
                (
                    provider_name,
                    lambda provider=provider:
                    provider.check(
                        text=text,
                        language=language,
                    ),
                )
            )

        results = await self._run_many(
            calls
        )

        return self._build_generic_consensus(
            results,
            "grammar",
        )

    async def check_pronunciation(
        self,
        text: str,
        language: str,
    ) -> ConsensusResult:

        if not text or not text.strip():

            return ConsensusResult(
                value=None,
                confidence=0.0,
                status="FAIL",
                providers_used=[],
                successful_providers=0,
                failed_providers=0,
                unsupported_providers=0,
                disagreement=False,
                details=[
                    "Input text is empty."
                ],
            )

        language = language.strip().lower()

        calls = []

        for provider in (
            self.registry.pronunciation_providers
        ):

            provider_name = (
                self._get_provider_name(
                    provider
                )
            )

            if not provider_name:
                continue

            if not self._provider_available(
                provider,
                language,
                "pronunciation",
            ):
                continue

            calls.append(
                (
                    provider_name,
                    lambda provider=provider:
                    provider.check(
                        text=text,
                        language=language,
                    ),
                )
            )

        results = await self._run_many(
            calls
        )

        return self._build_generic_consensus(
            results,
            "pronunciation",
        )

    async def full_quality_check(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> dict[str, Any]:

        translation = await self.translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )

        translated_text = translation.value

        if not translated_text:

            return {
                "translation": translation,
                "dictionary": None,
                "grammar": None,
                "pronunciation": None,
                "overall_confidence": 0.0,
                "status": "FAIL",
            }

        dictionary_result = (
            await self.check_dictionary(
                text=str(translated_text),
                language=target_language,
            )
        )

        grammar_result = (
            await self.check_grammar(
                text=str(translated_text),
                language=target_language,
            )
        )

        pronunciation_result = (
            await self.check_pronunciation(
                text=str(translated_text),
                language=target_language,
            )
        )

        quality_scores = [
            translation.confidence,
            dictionary_result.confidence,
            grammar_result.confidence,
            pronunciation_result.confidence,
        ]

        valid_scores = [
            score
            for score in quality_scores
            if score > 0
        ]

        if valid_scores:

            overall_confidence = round(
                sum(valid_scores)
                / len(valid_scores),
                2,
            )

        else:

            overall_confidence = 0.0

        status = (
            self._status_from_confidence(
                overall_confidence
            )
        )

        return {
            "translation": translation,
            "dictionary": dictionary_result,
            "grammar": grammar_result,
            "pronunciation": pronunciation_result,
            "overall_confidence": overall_confidence,
            "status": status,
        }

    def _provider_available(
        self,
        provider,
        language: str,
        capability: str,
    ) -> bool:

        info = getattr(
            provider,
            "info",
            None,
        )

        if info is None:

            return True

        if not isinstance(
            info,
            ProviderInfo,
        ):

            return True

        if not getattr(
            info,
            "enabled",
            True,
        ):

            return False

        try:

            return self.registry.manager.supports(
                provider_name=info.name,
                language=language,
                capability=capability,
            )

        except Exception:

            return True

    def _build_translation_consensus(
        self,
        results: list[ProviderResult],
    ) -> ConsensusResult:

        successful = [
            result
            for result in results
            if result.status
            == ProviderStatus.SUCCESS
            and result.value is not None
            and str(result.value).strip()
        ]

        failed = [
            result
            for result in results
            if result.status
            == ProviderStatus.FAILED
        ]

        unsupported = [
            result
            for result in results
            if result.status
            == ProviderStatus.UNSUPPORTED
        ]

        if not successful:

            details = [
                "No translation provider "
                "returned a usable result."
            ]

            if failed:

                details.append(
                    f"{len(failed)} provider(s) failed."
                )

            if unsupported:

                details.append(
                    f"{len(unsupported)} provider(s) "
                    "are unsupported."
                )

            return ConsensusResult(
                value=None,
                confidence=0.0,
                status="FAIL",
                providers_used=[],
                successful_providers=0,
                failed_providers=len(failed),
                unsupported_providers=len(
                    unsupported
                ),
                disagreement=False,
                details=details,
            )

        groups: dict[
            str,
            list[ProviderResult],
        ] = {}

        for result in successful:

            normalized = (
                self._normalize_text(
                    str(result.value)
                )
            )

            groups.setdefault(
                normalized,
                [],
            ).append(result)

        ranked_groups = sorted(
            groups.items(),
            key=lambda item: (
                len(item[1]),
                sum(
                    self._normalize_confidence(
                        result.confidence
                    )
                    for result in item[1]
                ),
                sum(
                    self._provider_quality_score(
                        result
                    )
                    for result in item[1]
                ),
            ),
            reverse=True,
        )

        _, best_results = (
            ranked_groups[0]
        )

        disagreement = len(groups) > 1

        confidence = (
            self._calculate_confidence(
                best_results=best_results,
                successful_count=len(
                    successful
                ),
                disagreement=disagreement,
            )
        )

        status = (
            self._status_from_confidence(
                confidence
            )
        )

        details: list[str] = []

        if disagreement:

            details.append(
                "Translation providers disagree."
            )

            details.append(
                f"{len(groups)} different "
                "translation candidates were detected."
            )

        else:

            details.append(
                "Translation providers agree "
                "on the selected result."
            )

        if failed:

            details.append(
                f"{len(failed)} provider(s) "
                "failed."
            )

        if unsupported:

            details.append(
                f"{len(unsupported)} provider(s) "
                "are unsupported."
            )

        return ConsensusResult(
            value=best_results[0].value,
            confidence=confidence,
            status=status,
            providers_used=[
                result.provider
                for result in successful
            ],
            successful_providers=len(
                successful
            ),
            failed_providers=len(
                failed
            ),
            unsupported_providers=len(
                unsupported
            ),
            disagreement=disagreement,
            details=details,
        )

    def _build_generic_consensus(
        self,
        results: list[ProviderResult],
        check_type: str,
    ) -> ConsensusResult:

        successful = [
            result
            for result in results
            if result.status
            == ProviderStatus.SUCCESS
            and result.value is not None
        ]

        failed = [
            result
            for result in results
            if result.status
            == ProviderStatus.FAILED
        ]

        unsupported = [
            result
            for result in results
            if result.status
            == ProviderStatus.UNSUPPORTED
        ]

        if not successful:

            return ConsensusResult(
                value=None,
                confidence=0.0,
                status="FAIL",
                providers_used=[],
                successful_providers=0,
                failed_providers=len(failed),
                unsupported_providers=len(
                    unsupported
                ),
                disagreement=False,
                details=[
                    f"No {check_type} provider "
                    "returned a usable result."
                ],
            )

        normalized_groups: dict[
            str,
            list[ProviderResult],
        ] = {}

        for result in successful:

            normalized = (
                self._normalize_text(
                    str(result.value)
                )
            )

            normalized_groups.setdefault(
                normalized,
                [],
            ).append(result)

        ranked_groups = sorted(
            normalized_groups.items(),
            key=lambda item: (
                len(item[1]),
                sum(
                    self._normalize_confidence(
                        result.confidence
                    )
                    for result in item[1]
                ),
            ),
            reverse=True,
        )

        _, best_results = (
            ranked_groups[0]
        )

        disagreement = (
            len(normalized_groups) > 1
        )

        confidence = (
            self._calculate_confidence(
                best_results=best_results,
                successful_count=len(
                    successful
                ),
                disagreement=disagreement,
            )
        )

        status = (
            self._status_from_confidence(
                confidence
            )
        )

        details: list[str] = []

        if disagreement:

            details.append(
                f"{check_type.capitalize()} "
                "providers returned different results."
            )

        else:

            details.append(
                f"{check_type.capitalize()} "
                "providers agree."
            )

        return ConsensusResult(
            value=best_results[0].value,
            confidence=confidence,
            status=status,
            providers_used=[
                result.provider
                for result in successful
            ],
            successful_providers=len(
                successful
            ),
            failed_providers=len(
                failed
            ),
            unsupported_providers=len(
                unsupported
            ),
            disagreement=disagreement,
            details=details,
        )

    @staticmethod
    def _get_provider_name(
        provider,
    ) -> str:

        name = getattr(
            provider,
            "name",
            None,
        )

        if name:
            return str(name)

        info = getattr(
            provider,
            "info",
            None,
        )

        info_name = getattr(
            info,
            "name",
            None,
        )

        if info_name:
            return str(info_name)

        return provider.__class__.__name__

    @staticmethod
    def _normalize_text(
        text: str,
    ) -> str:

        return " ".join(
            text.strip()
            .lower()
            .split()
        )

    @staticmethod
    def _normalize_confidence(
        confidence: float,
    ) -> float:

        try:

            value = float(
                confidence
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

        if value <= 1.0:

            value *= 100.0

        return max(
            0.0,
            min(100.0, value),
        )

    @classmethod
    def _provider_quality_score(
        cls,
        result: ProviderResult,
    ) -> float:

        confidence = (
            cls._normalize_confidence(
                result.confidence
            )
        )

        score = max(
            0.0,
            float(result.score),
        )

        return (
            confidence * 0.8
            + score * 0.2
        )

    @classmethod
    def _calculate_confidence(
        cls,
        best_results: list[ProviderResult],
        successful_count: int,
        disagreement: bool,
    ) -> float:

        if not best_results:
            return 0.0

        if successful_count <= 0:
            return 0.0

        provider_confidence = (
            sum(
                cls._normalize_confidence(
                    result.confidence
                )
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

        if (
            disagreement
            and agreement_ratio < 0.5
        ):

            confidence -= 15.0

        elif (
            disagreement
            and agreement_ratio < 0.75
        ):

            confidence -= 7.0

        return round(
            max(
                0.0,
                min(
                    100.0,
                    confidence,
                ),
            ),
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


provider_registry = ProviderRegistry(
    manager=provider_manager
)


quality_orchestrator = QualityOrchestrator(
    registry=provider_registry,
    max_concurrency=10,
)
