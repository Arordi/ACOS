from __future__ import annotations

import asyncio
import os

from google.cloud import translate_v3

from i18n.adapters import (
    TranslationAdapter,
    provider_result,
)
from i18n.providers import (
    ModelInfo,
    ProviderInfo,
)


# ---------------------------------------------------------
# Google Cloud Translation
# ---------------------------------------------------------
#
# Supported Google models:
#
# 1. general/nmt
# 2. general/translation-llm
#
# The orchestrator can run these as separate models.
#
# Credentials must NOT be stored in GitHub.
# Use Google Application Default Credentials / Render secrets.
# ---------------------------------------------------------


# Languages supported by Google's NMT model that are
# relevant to ACOS's 30-language target.
#
# Google officially lists these language codes for NMT.
# Cantonese is "yue".
#
ACOS_GOOGLE_NMT_LANGUAGES = frozenset({
    "en",
    "hy",
    "zh",
    "hi",
    "es",
    "ar",
    "fr",
    "bn",
    "pt",
    "id",
    "ur",
    "ru",
    "de",
    "ja",
    "mr",
    "vi",
    "te",
    "tr",
    "ta",
    "ko",
    "fa",
    "it",
    "th",
    "tl",
    "ha",
    "sw",
    "yue",
    "gu",
    "kn",
    "pa",
})


# Translation LLM currently has a narrower published
# language list than NMT.
#
# Armenian and Hausa are currently listed by Google as
# experimental support for Translation LLM.
#
ACOS_GOOGLE_TLLM_LANGUAGES = frozenset({
    "en",
    "hy",
    "zh",
    "hi",
    "es",
    "ar",
    "fr",
    "bn",
    "pt",
    "id",
    "ur",
    "ru",
    "de",
    "ja",
    "mr",
    "vi",
    "te",
    "tr",
    "ta",
    "ko",
    "fa",
    "it",
    "th",
    "tl",
    "ha",
    "sw",
    "gu",
    "kn",
    "pa",
})


class GoogleTranslationProvider(
    TranslationAdapter
):
    """
    Google Cloud Translation provider for ACOS.

    Provides:
        - Google NMT
        - Google Translation LLM

    The orchestrator treats each model independently
    so their outputs can later be compared.
    """

    GOOGLE_PROVIDER_NAME = (
        "google_cloud_translation"
    )

    NMT_MODEL = "general/nmt"

    TLLM_MODEL = (
        "general/translation-llm"
    )

    @property
    def info(self) -> ProviderInfo:
        return ProviderInfo(
            name=self.GOOGLE_PROVIDER_NAME,
            provider_type="translation",

            priority=10,

            quality_weight=1.0,
            cost_weight=1.0,

            enabled=self.configured,

            supported_languages=(
                ACOS_GOOGLE_NMT_LANGUAGES
            ),

            capabilities=frozenset({
                "translation",
            }),

            description=(
                "Google Cloud Translation "
                "Advanced provider with NMT "
                "and Translation LLM models."
            ),
        )

    def __init__(self):
        super().__init__()

        self.project_id = (
            os.getenv(
                "GOOGLE_CLOUD_PROJECT"
            )
            or os.getenv(
                "GOOGLE_PROJECT_ID"
            )
        )

        self.location = os.getenv(
            "GOOGLE_CLOUD_LOCATION",
            "global",
        )

        self.client = None

        self.configured = bool(
            self.project_id
        )

        if self.configured:
            try:
                self.client = (
                    translate_v3
                    .TranslationServiceClient()
                )
            except Exception:
                self.client = None

    # -----------------------------------------------------
    # MODEL INFORMATION
    # -----------------------------------------------------

    def get_models(self) -> list[ModelInfo]:
        """
        Return Google models available to ACOS.

        The models are registered by bootstrap.py.
        """

        return [
            ModelInfo(
                name=(
                    "google_translation_nmt"
                ),
                provider_name=(
                    self.GOOGLE_PROVIDER_NAME
                ),
                model_type="translation",

                priority=10,
                quality_weight=0.95,
                cost_weight=0.80,

                enabled=True,

                supported_languages=(
                    ACOS_GOOGLE_NMT_LANGUAGES
                ),

                capabilities=frozenset({
                    "translation",
                }),

                description=(
                    "Google Cloud Translation "
                    "Neural Machine Translation "
                    "(general/nmt)."
                ),
            ),

            ModelInfo(
                name=(
                    "google_translation_llm"
                ),
                provider_name=(
                    self.GOOGLE_PROVIDER_NAME
                ),
                model_type="translation",

                priority=5,
                quality_weight=1.00,
                cost_weight=1.00,

                enabled=True,

                supported_languages=(
                    ACOS_GOOGLE_TLLM_LANGUAGES
                ),

                capabilities=frozenset({
                    "translation",
                }),

                description=(
                    "Google Cloud Translation "
                    "LLM "
                    "(general/translation-llm)."
                ),
            ),
        ]

    # -----------------------------------------------------
    # CONFIGURATION
    # -----------------------------------------------------

    def is_ready(self) -> bool:
        return bool(
            self.project_id
            and self.client is not None
        )

    # -----------------------------------------------------
    # MODEL RESOURCE
    # -----------------------------------------------------

    def _model_resource(
        self,
        model_id: str,
    ) -> str:

        parent = (
            f"projects/{self.project_id}"
            f"/locations/{self.location}"
        )

        return (
            f"{parent}/models/{model_id}"
        )

    # -----------------------------------------------------
    # MODEL TRANSL
