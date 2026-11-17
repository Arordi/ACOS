from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from i18n.languages import (
    get_language_count,
    get_supported_languages,
)
from i18n.orchestrator import (
    quality_orchestrator,
)
from i18n.providers import (
    provider_manager,
)
from i18n.validator import (
    validate_translation_structure,
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/i18n",
    tags=["Internationalization"],
)


# =========================================================
# REQUEST MODELS
# =========================================================

class TranslationRequest(BaseModel):
    """
    Translation request sent by the ACOS frontend.
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=100_000,
        description="Text to translate.",
    )

    source_language: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="Source language code, for example: en.",
    )

    target_language: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="Target language code, for example: hy.",
    )


# =========================================================
# INTERNAL HELPERS
# =========================================================

def _normalize_language_code(
    language: str,
) -> str:
    """
    Normalize language identifiers.

    Examples:
        EN     -> en
        en-US  -> en
        hy-AM  -> hy
        RU     -> ru
    """

    value = str(language or "").strip().lower()

    if not value:
        raise HTTPException(
            status_code=400,
            detail="Language code is required.",
        )

    return value.split("-")[0].split("_")[0]


def _get_language_map() -> dict[str, Any]:
    """
    Build a fast lookup table for supported languages.
    """

    result: dict[str, Any] = {}

    for language in get_supported_languages():
        code = str(language.code).strip().lower()

        result[code] = language

    return result


def _find_language(
    language_code: str,
):
    """
    Find a supported ACOS language.

    Supports both:
        hy
        hy-AM
        en
        en-US
    """

    normalized = _normalize_language_code(
        language_code
    )

    languages = _get_language_map()

    language = languages.get(normalized)

    if language is None:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Unsupported language.",
                "language": language_code,
                "supported_languages": sorted(
                    languages.keys()
                ),
            },
        )

    return language


# =========================================================
# UI TRANSLATION CATALOG
# =========================================================

UI_CATALOG: dict[str, dict[str, str]] = {
    "en": {
        "app_name": "ACOS",
        "studio": "Studio",
        "new_film": "New Film",
        "projects": "Projects",
        "script": "Script",
        "characters": "Characters",
        "storyboard": "Storyboard",
        "scenes": "Scenes",
        "video": "Video",
        "voice": "Voice",
        "music": "Music",
        "languages": "Languages",
        "dubbing": "Dubbing",
        "subtitles": "Subtitles",
        "render_film": "Render Film",
        "create_film": "Create Film",
        "create_new_film": "Create New Film",
        "import_script": "Import Script",
        "current_film": "Current Film",
        "film_preview": "Film Preview",
        "timeline": "Timeline",
        "final_film": "Final Film",
        "download": "Download",
        "download_film": "Download Film",
        "save": "Save",
        "cancel": "Cancel",
        "close": "Close",
        "loading": "Loading...",
        "ready": "Ready",
        "draft": "Draft",
        "idea": "Idea",
        "translation": "Translation",
        "generate": "Generate",
        "open": "Open",
        "delete": "Delete",
    },

    "hy": {
        "app_name": "ACOS",
        "studio": "Ստուդիա",
        "new_film": "Նոր ֆիլմ",
        "projects": "Նախագծեր",
        "script": "Սցենար",
        "characters": "Կերպարներ",
        "storyboard": "ՍթորիԲորդ",
        "scenes": "Տեսարաններ",
        "video": "Տեսանյութ",
        "voice": "Ձայն",
        "music": "Երաժշտություն",
        "languages": "Լեզուներ",
        "dubbing": "Դուբլյաժ",
        "subtitles": "Ենթագրեր",
        "render_film": "Ռենդեր ֆիլմ",
        "create_film": "Ստեղծել ֆիլմ",
        "create_new_film": "Ստեղծել նոր ֆիլմ",
        "import_script": "Ներմուծել սցենար",
        "current_film": "Ընթացիկ ֆիլմ",
        "film_preview": "Ֆիլմի նախադիտում",
        "timeline": "Ժամանակագիծ",
        "final_film": "Վերջնական ֆիլմ",
        "download": "Ներբեռնել",
        "download_film": "Ներբեռնել ֆիլմը",
        "save": "Պահպանել",
        "cancel": "Չեղարկել",
        "close": "Փակել",
        "loading": "Բեռնվում է...",
        "ready": "Պատրաստ է",
        "draft": "Սևագիր",
        "idea": "Գաղափար",
        "translation": "Թարգմանություն",
        "generate": "Ստեղծել",
        "open": "Բացել",
        "delete": "Ջնջել",
    },

    "ru": {
        "app_name": "ACOS",
        "studio": "Студия",
        "new_film": "Новый фильм",
        "projects": "Проекты",
        "script": "Сценарий",
        "characters": "Персонажи",
        "storyboard": "Раскадровка",
        "scenes": "Сцены",
        "video": "Видео",
        "voice": "Голос",
        "music": "Музыка",
        "languages": "Языки",
        "dubbing": "Дубляж",
        "subtitles": "Субтитры",
        "render_film": "Рендер фильма",
        "create_film": "Создать фильм",
        "create_new_film": "Создать новый фильм",
        "import_script": "Импортировать сценарий",
        "current_film": "Текущий фильм",
        "film_preview": "Предпросмотр фильма",
        "timeline": "Таймлайн",
        "final_film": "Финальный фильм",
        "download": "Скачать",
        "download_film": "Скачать фильм",
        "save": "Сохранить",
        "cancel": "Отмена",
        "close": "Закрыть",
        "loading": "Загрузка...",
        "ready": "Готово",
        "draft": "Черновик",
        "idea": "Идея",
        "translation": "Перевод",
        "generate": "Создать",
        "open": "Открыть",
        "delete": "Удалить",
    },

    "fr": {
        "app_name": "ACOS",
        "studio": "Studio",
        "new_film": "Nouveau film",
        "projects": "Projets",
        "script": "Scénario",
        "characters": "Personnages",
        "storyboard": "Storyboard",
        "scenes": "Scènes",
        "video": "Vidéo",
        "voice": "Voix",
        "music": "Musique",
        "languages": "Langues",
        "dubbing": "Doublage",
        "subtitles": "Sous-titres",
        "render_film": "Rendre le film",
        "create_film": "Créer un film",
        "create_new_film": "Créer un nouveau film",
        "import_script": "Importer le scénario",
        "current_film": "Film actuel",
        "film_preview": "Aperçu du film",
        "timeline": "Chronologie",
        "final_film": "Film final",
        "download": "Télécharger",
        "download_film": "Télécharger le film",
        "save": "Enregistrer",
        "cancel": "Annuler",
        "close": "Fermer",
        "loading": "Chargement...",
        "ready": "Prêt",
        "draft": "Brouillon",
        "idea": "Idée",
        "translation": "Traduction",
        "generate": "Générer",
        "open": "Ouvrir",
        "delete": "Supprimer",
    },

    "de": {
        "app_name": "ACOS",
        "studio": "Studio",
        "new_film": "Neuer Film",
        "projects": "Projekte",
        "script": "Drehbuch",
        "characters": "Figuren",
        "storyboard": "Storyboard",
        "scenes": "Szenen",
        "video": "Video",
        "voice": "Stimme",
        "music": "Musik",
        "languages": "Sprachen",
        "dubbing": "Synchronisation",
        "subtitles": "Untertitel",
        "render_film": "Film rendern",
        "create_film": "Film erstellen",
        "create_new_film": "Neuen Film erstellen",
        "import_script": "Drehbuch importieren",
        "current_film": "Aktueller Film",
        "film_preview": "Filmvorschau",
        "timeline": "Zeitleiste",
        "final_film": "Finaler Film",
        "download": "Herunterladen",
        "download_film": "Film herunterladen",
        "save": "Speichern",
        "cancel": "Abbrechen",
        "close": "Schließen",
        "loading": "Wird geladen...",
        "ready": "Bereit",
        "draft": "Entwurf",
        "idea": "Idee",
        "translation": "Übersetzung",
        "generate": "Generieren",
        "open": "Öffnen",
        "delete": "Löschen",
    },

    "es": {
        "app_name": "ACOS",
        "studio": "Estudio",
        "new_film": "Nueva película",
        "projects": "Proyectos",
        "script": "Guion",
        "characters": "Personajes",
        "storyboard": "Storyboard",
        "scenes": "Escenas",
        "video": "Vídeo",
        "voice": "Voz",
        "music": "Música",
        "languages": "Idiomas",
        "dubbing": "Doblaje",
        "subtitles": "Subtítulos",
        "render_film": "Renderizar película",
        "create_film": "Crear película",
        "create_new_film": "Crear nueva película",
        "import_script": "Importar guion",
        "current_film": "Película actual",
        "film_preview": "Vista previa",
        "timeline": "Línea de tiempo",
        "final_film": "Película final",
        "download": "Descargar",
        "download_film": "Descargar película",
        "save": "Guardar",
        "cancel": "Cancelar",
        "close": "Cerrar",
        "loading": "Cargando...",
        "ready": "Listo",
        "draft": "Borrador",
        "idea": "Idea",
        "translation": "Traducción",
        "generate": "Generar",
        "open": "Abrir",
        "delete": "Eliminar",
    },
}


# =========================================================
# LANGUAGE LIST
# =========================================================

@router.get("/languages")
def languages():
    """
    Return all languages supported by ACOS.

    This endpoint is used by the frontend language selector.
    """

    supported_languages = get_supported_languages()

    return {
        "status": "ok",
        "count": get_language_count(),
        "languages": [
            {
                "code": language.code,
                "name": language.name,
                "native_name": language.native_name,
                "locale": language.locale,
                "rtl": language.rtl,
            }
            for language in supported_languages
        ],
    }


# =========================================================
# UI CATALOG
# =========================================================

@router.get("/ui/{language_code}")
def ui_translations(
    language_code: str,
):
    """
    Return ACOS interface translations for a language.

    The frontend can use this endpoint to dynamically
    replace navigation, buttons, workflow labels, etc.
    """

    language = _find_language(
        language_code
    )

    code = _normalize_language_code(
        language.code
    )

    translations = UI_CATALOG.get(
        code
    )

    # For languages that do not yet have a local
    # catalog, return English as a safe fallback.
    if translations is None:
        translations = UI_CATALOG["en"].copy()

        fallback = True
    else:
        fallback = False

    return {
        "status": "ok",
        "language": {
            "code": language.code,
            "name": language.name,
            "native_name": language.native_name,
            "locale": language.locale,
            "rtl": language.rtl,
        },
        "fallback": fallback,
        "translations": translations,
    }


# =========================================================
# VALIDATION
# =========================================================

@router.get("/validate")
def validate():
    """
    Validate the current translation structure.
    """

    try:
        result = validate_translation_structure()

        return {
            "status": "ok",
            "validation": result,
        }

    except Exception as exc:
        return {
            "status": "error",
            "validation": {
                "valid": False,
                "error": str(exc),
            },
        }


# =========================================================
# PROVIDERS
# =========================================================

@router.get("/providers")
def providers():
    """
    Return the current ACOS provider and model registry.

    Useful for debugging and monitoring which
    translation providers are registered.
    """

    try:
        summary = provider_manager.summary()

        return {
            "status": "ok",
            "providers": summary,
        }

    except Exception as exc:
        return {
            "status": "error",
            "providers": [],
            "error": str(exc),
        }


# =========================================================
# TRANSLATION
# =========================================================

@router.post("/translate")
async def translate(
    request: TranslationRequest,
):
    """
    Translate text through the ACOS quality orchestrator.

    The orchestrator can use the registered providers,
    compare their results and calculate confidence.
    """

    source_language = _normalize_language_code(
        request.source_language
    )

    target_language = _normalize_language_code(
        request.target_language
    )

    # Validate source language.
    _find_language(
        source_language
    )

    # Validate target language.
    _find_language(
        target_language
    )

    if source_language == target_language:
        return {
            "status": "ok",
            "source_language": source_language,
            "target_language": target_language,
            "source_text": request.text,
            "translation": request.text,
            "confidence": 1.0,
            "providers_used": [],
            "successful_providers": [],
            "failed_providers": [],
            "unsupported_providers": [],
            "disagreement": False,
            "details": {
                "reason": "source_and_target_languages_are_identical"
            },
        }

    try:
        result = await quality_orchestrator.translate(
            text=request.text,
            source_language=source_language,
            target_language=target_language,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Translation failed.",
                "error": str(exc),
            },
        ) from exc

    return {
        "status": result.status,
        "source_language": source_language,
        "target_language": target_language,
        "source_text": request.text,
        "translation": result.value,
        "confidence": result.confidence,
        "providers_used": result.providers_used,
        "successful_providers": result.successful_providers,
        "failed_providers": result.failed_providers,
        "unsupported_providers": result.unsupported_providers,
        "disagreement": result.disagreement,
        "details": result.details,
    }


# =========================================================
# LANGUAGE INFORMATION
# =========================================================

@router.get("/languages/{language_code}")
def language_details(
    language_code: str,
):
    """
    Return detailed information about one supported language.
    """

    language = _find_language(
        language_code
    )

    code = _normalize_language_code(
        language.code
    )

    return {
        "status": "ok",
        "language": {
            "code": language.code,
            "normalized_code": code,
            "name": language.name,
            "native_name": language.native_name,
            "locale": language.locale,
            "rtl": language.rtl,
        },
        "ui_catalog_available": (
            code in UI_CATALOG
        ),
    }


# =========================================================
# HEALTH
# =========================================================

@router.get("/health")
def health():
    """
    Lightweight i18n subsystem health endpoint.
    """

    try:
        language_count = get_language_count()

        provider_summary = provider_manager.summary()

        return {
            "status": "ok",
            "service": "ACOS Internationalization",
            "languages": language_count,
            "ui_catalog_languages": len(
                UI_CATALOG
            ),
            "providers": provider_summary,
        }

    except Exception as exc:
        return {
            "status": "degraded",
            "service": "ACOS Internationalization",
            "error": str(exc),
        }
