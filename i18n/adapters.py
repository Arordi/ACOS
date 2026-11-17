from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from i18n.orchestrator import (
    ProviderResult,
    ProviderStatus,
)
from i18n.providers import (
    ProviderInfo,
)


@dataclass
class AdapterConfig:
    api_key: str | None = None
    endpoint: str | None = None
    enabled: bool = False


class BaseProviderAdapter(ABC):

    def __init__(
        self,
        config: AdapterConfig | None = None,
    ):
        self.config = config or AdapterConfig()

    @property
    @abstractmethod
    def info(self) -> ProviderInfo:
        pass

    def is_configured(self) -> bool:
        return bool(
            self.config.enabled
            and self.config.api_key
        )

    def unsupported(
        self,
        message: str = "",
    ) -> ProviderResult:

        return ProviderResult(
            provider=self.info.name,
            status=ProviderStatus.UNSUPPORTED,
            confidence=0.0,
            details=message
            or "Operation is not supported.",
        )

    def disabled(
        self,
        message: str = "",
    ) -> ProviderResult:

        return ProviderResult(
            provider=self.info.name,
            status=ProviderStatus.DISABLED,
            confidence=0.0,
            details=message
            or "Provider is disabled.",
        )

    def failed(
        self,
        message: str,
    ) -> ProviderResult:

        return ProviderResult(
            provider=self.info.name,
            status=ProviderStatus.FAILED,
            confidence=0.0,
            details=message,
        )


class TranslationAdapter(
    BaseProviderAdapter
):

    @abstractmethod
    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> ProviderResult:
        pass


class DictionaryAdapter(
    BaseProviderAdapter
):

    @abstractmethod
    async def check(
        self,
        text: str,
        language: str,
    ) -> ProviderResult:
        pass


class GrammarAdapter(
    BaseProviderAdapter
):

    @abstractmethod
    async def check(
        self,
        text: str,
        language: str,
    ) -> ProviderResult:
        pass


class PronunciationAdapter(
    BaseProviderAdapter
):

    @abstractmethod
    async def check(
        self,
        text: str,
        language: str,
        audio_path: str | None = None,
    ) -> ProviderResult:
        pass


class SpeechToTextAdapter(
    BaseProviderAdapter
):

    @abstractmethod
    async def transcribe(
        self,
        audio_path: str,
        language: str,
    ) -> ProviderResult:
        pass


class TextToSpeechAdapter(
    BaseProviderAdapter
):

    @abstractmethod
    async def synthesize(
        self,
        text: str,
        language: str,
        output_path: str,
    ) -> ProviderResult:
        pass


class SemanticAdapter(
    BaseProviderAdapter
):

    @abstractmethod
    async def check(
        self,
        source_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
    ) -> ProviderResult:
        pass


def provider_result(
    provider: str,
    value: Any = None,
    confidence: float = 0.0,
    score: float = 0.0,
    details: str = "",
    metadata: dict[str, Any] | None = None,
) -> ProviderResult:

    return ProviderResult(
        provider=provider,
        status=ProviderStatus.SUCCESS,
        value=value,
        confidence=confidence,
        score=score,
        details=details,
        metadata=metadata or {},
    )
