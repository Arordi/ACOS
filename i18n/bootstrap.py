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
    """
    Register all ACOS translation providers
    and their models.
    """

    # -------------------------------------------------
    # Google Cloud Translation
    # -------------------------------------------------

    google_provider = (
        GoogleTranslationProvider()
    )

    provider_manager.register(
        google_provider.info
    )

    provider_registry.register_translation(
        google_provider
    )

    # -------------------------------------------------
    # Google translation models
    # -------------------------------------------------

    for model in (
        google_provider.get_models()
    ):
        provider_manager.register_model(
            model
        )


# Register providers once when ACOS starts.
register_providers()
