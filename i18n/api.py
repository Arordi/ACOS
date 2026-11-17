from fastapi import APIRouter
from pydantic import BaseModel

from i18n.languages import (
    get_language_count,
    get_supported_languages,
)
from i18n.orchestrator import (
    quality_orchestrator,
)
from i18n.validator import (
    validate_translation_structure,
)


router = APIRouter(
    prefix="/api/i18n",
    tags=["Internationalization"],
)


class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


@router.get("/languages")
def languages():
    return {
        "count": get_language_count(),
        "languages": [
            {
                "code": language.code,
                "name": language.name,
                "native_name": language.native_name,
                "locale": language.locale,
                "rtl": language.rtl,
            }
            for language in get_supported_languages()
        ],
    }


@router.get("/validate")
def validate():
    return validate_translation_structure()


@router.post("/translate")
async def translate(
    request: TranslationRequest,
):
    result = await quality_orchestrator.translate(
        text=request.text,
        source_language=request.source_language,
        target_language=request.target_language,
    )

    return {
        "source_language":
            request.source_language,

        "target_language":
            request.target_language,

        "source_text":
            request.text,

        "translation":
            result.value,

        "confidence":
            result.confidence,

        "status":
            result.status,

        "providers_used":
            result.providers_used,

        "successful_providers":
            result.successful_providers,

        "failed_providers":
            result.failed_providers,

        "unsupported_providers":
            result.unsupported_providers,

        "disagreement":
            result.disagreement,

        "details":
            result.details,
    }
