from i18n.google_translation import (
    GoogleTranslationProvider,
)

from i18n.orchestrator import (
    provider_registry,
)

from i18n.providers import (
    provider_manager,
)


def register_providers() -> None:

    google_provider = (
        GoogleTranslationProvider()
    )

    provider_manager.register(
        google_provider.info
    )

    provider_registry.register_translation(
        google_provider
    )


register_providers()
