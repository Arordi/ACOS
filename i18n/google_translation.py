from __future__ import annotations

import asyncio
import os
from typing import Any

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
# ACOS Google Translation provider.
#
# Supported Google models:
#
# 1. general/nmt
# 2. general/translation-llm
#
# The orchestrator can use this provider together with
# other translation providers and compare their results.
#
# Credentials must NOT be stored in GitHub.
#
# Recommended configuration:
#
# GOOGLE_CLOUD_PROJECT
# GOOGLE_CLOUD_LOCATION
#
# Google Application Default Credentials should be
# configured through Render/environment secrets.
# ---------------------------------------------------------


# ---------------------------------------------------------
# ACOS GOOGLE NMT LANGUAGES
# ---------------------------------------------------------
#
# Languages relevant to ACOS's 30-language target.
#
# Google language codes are used here.
#
# Cantonese:
#     yue
#
# Mandarin Chinese:
#     zh
#
# Armenian:
#     hy
#
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# ACOS GOOGLE TRANSLATION LLM LANGUAGES
# ---------------------------------------------------------
#
# Keep this list separate from NMT so the orchestrator
# can make model-specific decisions.
#
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# ALL GOOGLE LANGUAGES
# ---------------------------------------------------------

ACOS_GOOGLE_LANGUAGES = frozenset(
    ACOS_GOOGLE_NMT_LANGUAGES
    | ACOS_GOOGLE_TLLM_LANGUAGES
)


class GoogleTranslationProvider(
    TranslationAdapter
):
    """
    Google Cloud Translation provider for ACOS.

    Provides:
        - Google Cloud Translation NMT
        - Google Cloud Translation LLM

    The provider exposes a single translate() interface
    required by TranslationAdapter.

    The actual model can be selected using the model_id
    parameter internally.

    The default translation model is NMT because it has
    the broadest language support in this ACOS provider.
    """

    GOOGLE_PROVIDER_NAME = (
        "google_cloud_translation"
    )

    NMT_MODEL = "general/nmt"

    TLLM_MODEL = (
        "general/translation-llm"
    )

    DEFAULT_MODEL = NMT_MODEL

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

        self.location = (
            os.getenv(
                "GOOGLE_CLOUD_LOCATION",
            )
            or "global"
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
    # PROVIDER INFORMATION
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # MODEL INFORMATION
    # -----------------------------------------------------

    def get_models(
        self,
    ) -> list[ModelInfo]:

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
    # LANGUAGE SUPPORT
    # -----------------------------------------------------

    def supports_language(
        self,
        language: str,
        model_id: str | None = None,
    ) -> bool:

        normalized = (
            self._normalize_language(
                language
            )
        )

        if model_id == self.TLLM_MODEL:

            return (
                normalized
                in ACOS_GOOGLE_TLLM_LANGUAGES
            )

        return (
            normalized
            in ACOS_GOOGLE_NMT_LANGUAGES
        )

    # -----------------------------------------------------
    # LANGUAGE NORMALIZATION
    # -----------------------------------------------------

    @staticmethod
    def _normalize_language(
        language: str,
    ) -> str:

        if not language:

            return ""

        normalized = (
            language
            .strip()
            .lower()
            .replace("_", "-")
        )

        aliases = {
            "zh-cn": "zh",
            "zh-sg": "zh",
            "zh-tw": "zh",
            "zh-hk": "zh",
            "cmn": "zh",
            "yue-hk": "yue",
            "iw": "he",
            "in": "id",
        }

        return aliases.get(
            normalized,
            normalized,
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
    # TRANSLATION
    # -----------------------------------------------------
    #
    # This is the abstract method required by
    # TranslationAdapter.
    #
    # This method is the reason Render previously failed
    # with:
    #
    # TypeError:
    # Can't instantiate abstract class
    # GoogleTranslationProvider without an implementation
    # for abstract method 'translate'
    #
    # -----------------------------------------------------

    async def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> Any:

        if not text or not text.strip():

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value="",
                confidence=0.0,
                details=(
                    "Input text is empty."
                ),
            )

        if not self.is_ready():

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Google Cloud Translation "
                    "is not configured."
                ),
            )

        source_language = (
            self._normalize_language(
                source_language
            )
        )

        target_language = (
            self._normalize_language(
                target_language
            )
        )

        if not source_language:

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Source language is missing."
                ),
            )

        if not target_language:

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Target language is missing."
                ),
            )

        if (
            target_language
            not in ACOS_GOOGLE_NMT_LANGUAGES
        ):

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Target language is not "
                    "supported by the configured "
                    "Google NMT language set."
                ),
                metadata={
                    "source_language": (
                        source_language
                    ),
                    "target_language": (
                        target_language
                    ),
                },
            )

        try:

            result = await self._translate_with_model(
                text=text,
                source_language=source_language,
                target_language=target_language,
                model_id=self.NMT_MODEL,
            )

            return result

        except asyncio.CancelledError:

            raise

        except Exception as exc:

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Google translation failed: "
                    f"{exc}"
                ),
                metadata={
                    "exception_type": (
                        type(exc).__name__
                    ),
                    "source_language": (
                        source_language
                    ),
                    "target_language": (
                        target_language
                    ),
                },
            )

    # -----------------------------------------------------
    # TRANSLATION WITH SPECIFIC MODEL
    # -----------------------------------------------------

    async def _translate_with_model(
        self,
        text: str,
        source_language: str,
        target_language: str,
        model_id: str,
    ) -> Any:

        if not self.is_ready():

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Google Cloud client "
                    "is not ready."
                ),
            )

        if not self.supports_language(
            target_language,
            model_id=model_id,
        ):

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    f"Language '{target_language}' "
                    f"is not supported by model "
                    f"'{model_id}'."
                ),
            )

        parent = (
            f"projects/{self.project_id}"
            f"/locations/{self.location}"
        )

        model_resource = (
            self._model_resource(
                model_id
            )
        )

        request = (
            translate_v3.TranslateTextRequest(
                parent=parent,

                source_language_code=(
                    source_language
                ),

                target_language_code=(
                    target_language
                ),

                contents=[
                    text
                ],

                mime_type="text/plain",

                model=model_resource,
            )
        )

        loop = asyncio.get_running_loop()

        response = await loop.run_in_executor(
            None,
            self.client.translate_text,
            request,
        )

        translations = getattr(
            response,
            "translations",
            None,
        )

        if not translations:

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Google returned no "
                    "translation."
                ),
                metadata={
                    "model": model_id,
                },
            )

        translated_text = (
            translations[0].translated_text
        )

        if not translated_text:

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Google returned an empty "
                    "translation."
                ),
                metadata={
                    "model": model_id,
                },
            )

        return provider_result(
            provider=self.GOOGLE_PROVIDER_NAME,
            value=translated_text,
            confidence=95.0,
            details=(
                "Google Cloud Translation "
                f"completed using {model_id}."
            ),
            metadata={
                "model": model_id,
                "source_language": (
                    source_language
                ),
                "target_language": (
                    target_language
                ),
            },
        )

    # -----------------------------------------------------
    # NMT TRANSLATION
    # -----------------------------------------------------

    async def translate_nmt(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> Any:

        return await self._translate_with_model(
            text=text,
            source_language=(
                self._normalize_language(
                    source_language
                )
            ),
            target_language=(
                self._normalize_language(
                    target_language
                )
            ),
            model_id=self.NMT_MODEL,
        )

    # -----------------------------------------------------
    # TRANSLATION LLM
    # -----------------------------------------------------

    async def translate_llm(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> Any:

        source_language = (
            self._normalize_language(
                source_language
            )
        )

        target_language = (
            self._normalize_language(
                target_language
            )
        )

        if not self.is_ready():

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Google Cloud client "
                    "is not ready."
                ),
            )

        if not self.supports_language(
            target_language,
            model_id=self.TLLM_MODEL,
        ):

            return provider_result(
                provider=self.GOOGLE_PROVIDER_NAME,
                value=None,
                confidence=0.0,
                details=(
                    "Target language is not "
                    "supported by Google "
                    "Translation LLM."
                ),
            )

        return await self._translate_with_model(
            text=text,
            source_language=source_language,
            target_language=target_language,
            model_id=self.TLLM_MODEL,
        )

    # -----------------------------------------------------
    # TRANSLATE BOTH MODELS
    # -----------------------------------------------------
    #
    # This method is useful for ACOS quality checking.
    #
    # NMT and Translation LLM can be executed separately,
    # and the orchestrator can later compare their results.
    #
    # -----------------------------------------------------

    async def translate_with_all_models(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> list[Any]:

        tasks = [
            self.translate_nmt(
                text=text,
                source_language=source_language,
                target_language=target_language,
            ),
        ]

        normalized_target = (
            self._normalize_language(
                target_language
            )
        )

        if (
            normalized_target
            in ACOS_GOOGLE_TLLM_LANGUAGES
        ):

            tasks.append(
                self.translate_llm(
                    text=text,
                    source_language=source_language,
                    target_language=target_language,
                )
            )

        return list(
            await asyncio.gather(
                *tasks,
                return_exceptions=False,
            )
        )

    # -----------------------------------------------------
    # HEALTH INFORMATION
    # -----------------------------------------------------

    def health(self) -> dict[str, Any]:

        return {
            "provider": (
                self.GOOGLE_PROVIDER_NAME
            ),
            "configured": self.configured,
            "ready": self.is_ready(),
            "project_id_configured": bool(
                self.project_id
            ),
            "location": self.location,
            "client_available": (
                self.client is not None
            ),
            "models": [
                {
                    "name": model.name,
                    "enabled": model.enabled,
                    "languages": len(
                        model.supported_languages
                    ),
                }
                for model in self.get_models()
            ],
        }
