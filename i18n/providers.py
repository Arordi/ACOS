from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ProviderInfo:
    name: str
    provider_type: str

    priority: int = 100
    quality_weight: float = 1.0
    cost_weight: float = 1.0

    enabled: bool = True

    supported_languages: frozenset[str] = frozenset()
    capabilities: frozenset[str] = frozenset()

    description: str = ""


class BaseProvider(Protocol):

    @property
    def info(self) -> ProviderInfo:
        ...


class ProviderManager:

    def __init__(self):
        self._providers: dict[str, ProviderInfo] = {}

    def register(
        self,
        provider: ProviderInfo,
    ) -> None:

        self._providers[provider.name] = provider

    def unregister(
        self,
        provider_name: str,
    ) -> None:

        self._providers.pop(
            provider_name,
            None,
        )

    def get(
        self,
        provider_name: str,
    ) -> ProviderInfo | None:

        return self._providers.get(
            provider_name
        )

    def all(
        self,
    ) -> list[ProviderInfo]:

        return list(
            self._providers.values()
        )

    def enabled(
        self,
    ) -> list[ProviderInfo]:

        return [
            provider
            for provider in self._providers.values()
            if provider.enabled
        ]

    def supports(
        self,
        provider_name: str,
        language: str,
        capability: str,
    ) -> bool:

        provider = self.get(
            provider_name
        )

        if provider is None:
            return False

        if not provider.enabled:
            return False

        if (
            provider.supported_languages
            and language not in provider.supported_languages
        ):
            return False

        return capability in provider.capabilities

    def available_for(
        self,
        language: str,
        capability: str,
    ) -> list[ProviderInfo]:

        providers = [
            provider
            for provider in self.enabled()
            if (
                (
                    not provider.supported_languages
                    or language
                    in provider.supported_languages
                )
                and capability
                in provider.capabilities
            )
        ]

        return sorted(
            providers,
            key=lambda provider: (
                -provider.quality_weight,
                provider.priority,
                provider.cost_weight,
            ),
        )

    def summary(self) -> dict[str, Any]:

        providers = self.all()

        return {
            "count": len(providers),
            "enabled": sum(
                1
                for provider in providers
                if provider.enabled
            ),
            "disabled": sum(
                1
                for provider in providers
                if not provider.enabled
            ),
            "providers": [
                {
                    "name": provider.name,
                    "type": provider.provider_type,
                    "enabled": provider.enabled,
                    "priority": provider.priority,
                    "quality_weight": (
                        provider.quality_weight
                    ),
                    "cost_weight": (
                        provider.cost_weight
                    ),
                    "languages": sorted(
                        provider.supported_languages
                    ),
                    "capabilities": sorted(
                        provider.capabilities
                    ),
                }
                for provider in providers
            ],
        }


provider_manager = ProviderManager()
