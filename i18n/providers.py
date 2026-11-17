from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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


@dataclass(frozen=True)
class ModelInfo:
    name: str
    provider_name: str

    model_type: str

    priority: int = 100
    quality_weight: float = 1.0
    cost_weight: float = 1.0

    enabled: bool = True

    supported_languages: frozenset[str] = frozenset()
    capabilities: frozenset[str] = frozenset()

    description: str = ""


class ProviderManager:

    def __init__(self):
        self._providers: dict[
            str,
            ProviderInfo,
        ] = {}

        self._models: dict[
            str,
            ModelInfo,
        ] = {}

    def register(
        self,
        provider: ProviderInfo,
    ) -> None:

        self._providers[
            provider.name
        ] = provider

    def unregister(
        self,
        provider_name: str,
    ) -> None:

        self._providers.pop(
            provider_name,
            None,
        )

        models_to_remove = [
            model_name
            for model_name, model
            in self._models.items()
            if model.provider_name
            == provider_name
        ]

        for model_name in models_to_remove:
            self._models.pop(
                model_name,
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
            for provider
            in self._providers.values()
            if provider.enabled
        ]

    def register_model(
        self,
        model: ModelInfo,
    ) -> None:

        if model.provider_name not in (
            self._providers
        ):
            raise ValueError(
                "Cannot register model "
                f"'{model.name}'. Provider "
                f"'{model.provider_name}' "
                "is not registered."
            )

        self._models[
            model.name
        ] = model

    def unregister_model(
        self,
        model_name: str,
    ) -> None:

        self._models.pop(
            model_name,
            None,
        )

    def get_model(
        self,
        model_name: str,
    ) -> ModelInfo | None:

        return self._models.get(
            model_name
        )

    def all_models(
        self,
    ) -> list[ModelInfo]:

        return list(
            self._models.values()
        )

    def enabled_models(
        self,
    ) -> list[ModelInfo]:

        return [
            model
            for model
            in self._models.values()
            if model.enabled
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
            and language
            not in provider.supported_languages
        ):
            return False

        return (
            capability
            in provider.capabilities
        )

    def model_supports(
        self,
        model_name: str,
        language: str,
        capability: str,
    ) -> bool:

        model = self.get_model(
            model_name
        )

        if model is None:
            return False

        if not model.enabled:
            return False

        if (
            model.supported_languages
            and language
            not in model.supported_languages
        ):
            return False

        return (
            capability
            in model.capabilities
        )

    def available_for(
        self,
        language: str,
        capability: str,
    ) -> list[ProviderInfo]:

        providers = [
            provider
            for provider
            in self.enabled()
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

    def available_models_for(
        self,
        language: str,
        capability: str,
    ) -> list[ModelInfo]:

        models = [
            model
            for model
            in self.enabled_models()
            if (
                (
                    not model.supported_languages
                    or language
                    in model.supported_languages
                )
                and capability
                in model.capabilities
            )
        ]

        return sorted(
            models,
            key=lambda model: (
                -model.quality_weight,
                model.priority,
                model.cost_weight,
            ),
        )

    def summary(
        self,
    ) -> dict[str, Any]:

        providers = self.all()
        models = self.all_models()

        return {
            "providers": {
                "count": len(providers),
                "enabled": sum(
                    1
                    for provider
                    in providers
                    if provider.enabled
                ),
                "disabled": sum(
                    1
                    for provider
                    in providers
                    if not provider.enabled
                ),
            },
            "models": {
                "count": len(models),
                "enabled": sum(
                    1
                    for model
                    in models
                    if model.enabled
                ),
                "disabled": sum(
                    1
                    for model
                    in models
                    if not model.enabled
                ),
            },
            "provider_list": [
                {
                    "name": provider.name,
                    "type": provider.provider_type,
                    "enabled": provider.enabled,
                    "priority": provider.priority,
                    "quality_weight":
                        provider.quality_weight,
                    "cost_weight":
                        provider.cost_weight,
                    "languages": sorted(
                        provider.supported_languages
                    ),
                    "capabilities": sorted(
                        provider.capabilities
                    ),
                }
                for provider in providers
            ],
            "model_list": [
                {
                    "name": model.name,
                    "provider":
                        model.provider_name,
                    "type": model.model_type,
                    "enabled": model.enabled,
                    "priority": model.priority,
                    "quality_weight":
                        model.quality_weight,
                    "cost_weight":
                        model.cost_weight,
                    "languages": sorted(
                        model.supported_languages
                    ),
                    "capabilities": sorted(
                        model.capabilities
                    ),
                }
                for model in models
            ],
        }


provider_manager = ProviderManager()
