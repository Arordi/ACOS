from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from i18n.languages import (
    get_language_count,
    get_supported_languages,
)
from i18n.orchestrator import quality_orchestrator
from i18n.providers import provider_manager
from i18n.validator import validate_translation_structure


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/i18n",
    tags=["Internationalization"],
)


# =========================================================
# UI TRANSLATION CATALOG
# =========================================================

UI_CATALOG: dict[str, dict[str, str]] = {
    "en": {
        "app_name": "ACOS",
        "studio": "Studio",
        "new_film": "New Film",
        "create_film": "Create Film",
        "create_new_film": "Create New Film",
        "projects": "Projects",
        "project": "Project",
        "script": "Script",
        "characters": "Characters",
        "storyboard": "Storyboard",
        "scenes": "Scenes",
        "video": "Video",
        "voice": "Voice",
        "music": "Music",
        "languages": "Languages",
        "translation": "Translation",
        "dubbing": "Dubbing",
        "subtitles": "Subtitles",
        "render": "Render",
        "render_film": "Render Film",
        "media": "Media",
        "upload": "Upload",
        "download": "Download",
        "download_film": "Download Film",
        "save": "Save",
        "cancel": "Cancel",
        "close": "Close",
        "delete": "Delete",
        "edit": "Edit",
        "open": "Open",
        "back": "Back",
        "next": "Next",
        "continue": "Continue",
        "generate": "Generate",
        "loading": "Loading...",
        "processing": "Processing...",
        "ready": "Ready",
        "draft": "Draft",
        "idea": "Idea",
        "workflow": "Workflow",
        "current_film": "Current Film",
        "film_preview": "Film Preview",
        "timeline": "Timeline",
        "final_film": "Final Film",
        "name": "Name",
        "description": "Description",
        "project_type": "Project Type",
        "created": "Created",
        "updated": "Updated",
        "success": "Success",
        "error": "Error",
        "retry": "Retry",
        "no_projects": "No projects yet",
        "server_error": "Server error",
        "network_error": "Network error",
    },

    "hy": {
        "app_name": "ACOS",
        "studio": "Ստուդիա",
        "new_film": "Նոր ֆիլմ",
        "create_film": "Ստեղծել ֆիլմ",
        "create_new_film": "Ստեղծել նոր ֆիլմ",
        "projects": "Նախագծեր",
        "project": "Նախագիծ",
        "script": "Սցենար",
        "characters": "Կերպարներ",
        "storyboard": "ՍթորիԲորդ",
        "scenes": "Տեսարաններ",
        "video": "Տեսանյութ",
        "voice": "Ձայն",
        "music": "Երաժշտություն",
        "languages": "Լեզուներ",
        "translation": "Թարգմանություն",
        "dubbing": "Դուբլյաժ",
        "subtitles": "Ենթագրեր",
        "render": "Ռենդեր",
        "render_film": "Ռենդեր ֆիլմ",
        "media": "Մեդիա",
        "upload": "Վերբեռնել",
        "download": "Ներբեռնել",
        "download_film": "Ներբեռնել ֆիլմը",
        "save": "Պահպանել",
        "cancel": "Չեղարկել",
        "close": "Փակել",
        "delete": "Ջնջել",
        "edit": "Խմբագրել",
        "open": "Բացել",
        "back": "Հետ",
        "next": "Հաջորդը",
        "continue": "Շարունակել",
        "generate": "Ստեղծել",
        "loading": "Բեռնվում է...",
        "processing": "Մշակվում է...",
        "ready": "Պատրաստ է",
        "draft": "Սևագիր",
        "idea": "Գաղափար",
        "workflow": "Աշխատանքային գործընթաց",
        "current_film": "Ընթացիկ ֆիլմ",
        "film_preview": "Ֆիլմի նախադիտում",
        "timeline": "Ժամանակագիծ",
        "final_film": "Վերջնական ֆիլմ",
        "name": "Անուն",
        "description": "Նկարագրություն",
        "project_type": "Նախագծի տեսակ",
        "created": "Ստեղծվել է",
        "updated": "Թարմացվել է",
        "success": "Հաջողություն",
        "error": "Սխալ",
        "retry": "Կրկին փորձել",
        "no_projects": "Դեռևս նախագծեր չկան",
        "server_error": "Սերվերի սխալ",
        "network_error": "Ցանցային սխալ",
    },

    "ru": {
        "app_name": "ACOS",
        "studio": "Студия",
        "new_film": "Новый фильм",
        "create_film": "Создать фильм",
        "create_new_film": "Создать новый фильм",
        "projects": "Проекты",
        "project": "Проект",
        "script": "Сценарий",
        "characters": "Персонажи",
        "storyboard": "Раскадровка",
        "scenes": "Сцены",
        "video": "Видео",
        "voice": "Голос",
        "music": "Музыка",
        "languages": "Языки",
        "translation": "Перевод",
        "dubbing": "Дубляж",
        "subtitles": "Субтитры",
        "render": "Рендер",
        "render_film": "Рендер фильма",
        "media": "Медиа",
        "upload": "Загрузить",
        "download": "Скачать",
        "download_film": "Скачать фильм",
        "save": "Сохранить",
        "cancel": "Отмена",
        "close": "Закрыть",
        "delete": "Удалить",
        "edit": "Изменить",
        "open": "Открыть",
        "back": "Назад",
        "next": "Далее",
        "continue": "Продолжить",
        "generate": "Создать",
        "loading": "Загрузка...",
        "processing": "Обработка...",
        "ready": "Готово",
        "draft": "Черновик",
        "idea": "Идея",
        "workflow": "Рабочий процесс",
        "current_film": "Текущий фильм",
        "film_preview": "Предпросмотр фильма",
        "timeline": "Таймлайн",
        "final_film": "Финальный фильм",
        "name": "Название",
        "description": "Описание",
        "project_type": "Тип проекта",
        "created": "Создано",
        "updated": "Обновлено",
        "success": "Успешно",
        "error": "Ошибка",
        "retry": "Повторить",
        "no_projects": "Проектов пока нет",
        "server_error": "Ошибка сервера",
        "network_error": "Ошибка сети",
    },

    "fr": {
        "app_name": "ACOS",
        "studio": "Studio",
        "new_film": "Nouveau film",
        "create_film": "Créer un film",
        "create_new_film": "Créer un nouveau film",
        "projects": "Projets",
        "project": "Projet",
        "script": "Scénario",
        "characters": "Personnages",
        "storyboard": "Storyboard",
        "scenes": "Scènes",
        "video": "Vidéo",
        "voice": "Voix",
        "music": "Musique",
        "languages": "Langues",
        "translation": "Traduction",
        "dubbing": "Doublage",
        "subtitles": "Sous-titres",
        "render": "Rendu",
        "render_film": "Rendre le film",
        "media": "Média",
        "upload": "Télécharger",
        "download": "Télécharger",
        "download_film": "Télécharger le film",
        "save": "Enregistrer",
        "cancel": "Annuler",
        "close": "Fermer",
        "delete": "Supprimer",
        "edit": "Modifier",
        "open": "Ouvrir",
        "back": "Retour",
        "next": "Suivant",
        "continue": "Continuer",
        "generate": "Générer",
        "loading": "Chargement...",
        "processing": "Traitement...",
        "ready": "Prêt",
        "draft": "Brouillon",
        "idea": "Idée",
        "workflow": "Flux de travail",
        "current_film": "Film actuel",
        "film_preview": "Aperçu du film",
        "timeline": "Chronologie",
        "final_film": "Film final",
        "name": "Nom",
        "description": "Description",
        "project_type": "Type de projet",
        "created": "Créé",
        "updated": "Mis à jour",
        "success": "Succès",
        "error": "Erreur",
        "retry": "Réessayer",
        "no_projects": "Aucun projet",
        "server_error": "Erreur serveur",
        "network_error": "Erreur réseau",
    },

    "de": {
        "app_name": "ACOS",
        "studio": "Studio",
        "new_film": "Neuer Film",
        "create_film": "Film erstellen",
        "create_new_film": "Neuen Film erstellen",
        "projects": "Projekte",
        "project": "Projekt",
        "script": "Drehbuch",
        "characters": "Figuren",
        "storyboard": "Storyboard",
        "scenes": "Szenen",
        "video": "Video",
        "voice": "Stimme",
        "music": "Musik",
        "languages": "Sprachen",
        "translation": "Übersetzung",
        "dubbing": "Synchronisation",
        "subtitles": "Untertitel",
        "render": "Rendern",
        "render_film": "Film rendern",
        "media": "Medien",
        "upload": "Hochladen",
        "download": "Herunterladen",
        "download_film": "Film herunterladen",
        "save": "Speichern",
        "cancel": "Abbrechen",
        "close": "Schließen",
        "delete": "Löschen",
        "edit": "Bearbeiten",
        "open": "Öffnen",
        "back": "Zurück",
        "next": "Weiter",
        "continue": "Fortfahren",
        "generate": "Generieren",
        "loading": "Wird geladen...",
        "processing": "Verarbeitung...",
        "ready": "Bereit",
        "draft": "Entwurf",
        "idea": "Idee",
        "workflow": "Workflow",
        "current_film": "Aktueller Film",
        "film_preview": "Filmvorschau",
        "timeline": "Zeitleiste",
        "final_film": "Finaler Film",
        "name": "Name",
        "description": "Beschreibung",
        "project_type": "Projekttyp",
        "created": "Erstellt",
        "updated": "Aktualisiert",
        "success": "Erfolgreich",
        "error": "Fehler",
        "retry": "Erneut versuchen",
        "no_projects": "Noch keine Projekte",
        "server_error": "Serverfehler",
        "network_error": "Netzwerkfehler",
    },

    "es": {
        "app_name": "ACOS",
        "studio": "Estudio",
        "new_film": "Nueva película",
        "create_film": "Crear película",
        "create_new_film": "Crear nueva película",
        "projects": "Proyectos",
        "project": "Proyecto",
        "script": "Guion",
        "characters": "Personajes",
        "storyboard": "Storyboard",
        "scenes": "Escenas",
        "video": "Vídeo",
        "voice": "Voz",
        "music": "Música",
        "languages": "Idiomas",
        "translation": "Traducción",
        "dubbing": "Doblaje",
        "subtitles": "Subtítulos",
        "render": "Renderizar",
        "render_film": "Renderizar película",
        "media": "Medios",
        "upload": "Subir",
        "download": "Descargar",
        "download_film": "Descargar película",
        "save": "Guardar",
        "cancel": "Cancelar",
        "close": "Cerrar",
        "delete": "Eliminar",
        "edit": "Editar",
        "open": "Abrir",
        "back": "Atrás",
        "next": "Siguiente",
        "continue": "Continuar",
        "generate": "Generar",
        "loading": "Cargando...",
        "processing": "Procesando...",
        "ready": "Listo",
        "draft": "Borrador",
        "idea": "Idea",
        "workflow": "Flujo de trabajo",
        "current_film": "Película actual",
        "film_preview": "Vista previa",
        "timeline": "Línea de tiempo",
        "final_film": "Película final",
        "name": "Nombre",
        "description": "Descripción",
        "project_type": "Tipo de proyecto",
        "created": "Creado",
        "updated": "Actualizado",
        "success": "Éxito",
        "error": "Error",
        "retry": "Reintentar",
        "no_projects": "No hay proyectos",
        "server_error": "Error del servidor",
        "network_error": "Error de red",
    },
}


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
    )

    source_language: str = Field(
        default="auto",
        min_length=2,
        max_length=20,
    )

    target_language: str = Field(
        ...,
        min_length=2,
        max_length=20,
    )


# =========================================================
# INTERNAL HELPERS
# =========================================================

def _normalize_language_code(language: str) -> str:
    """
    Normalize language identifiers.

    Examples:

        EN       -> en
        en-US    -> en
        hy-AM    -> hy
        RU       -> ru
    """

    value = str(language or "").strip().lower()

    if not value:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "language_required",
                "message": "Language code is required.",
            },
        )

    return value.split("-")[0].split("_")[0]


def _get_language_map() -> dict[str, Any]:
    """
    Build a fast language lookup table.
    """

    result: dict[str, Any] = {}

    try:
        supported = get_supported_languages()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "language_registry_unavailable",
                "message": "Language registry is unavailable.",
                "reason": str(exc),
            },
        ) from exc

    for language in supported:
        code = str(
            getattr(language, "code", "")
        ).strip().lower()

        if code:
            result[code] = language

    return result


def _find_language(language_code: str):
    """
    Find a supported ACOS language.
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
                "error": "unsupported_language",
                "message": "Unsupported language.",
                "language": language_code,
                "supported_languages": sorted(
                    languages.keys()
                ),
            },
        )

    return language


def _safe_language_value(
    language: Any,
    attribute: str,
    default: Any = None,
) -> Any:
    """
    Safely read an optional language property.

    This prevents the API from crashing if a future
    Language model changes slightly.
    """

    return getattr(
        language,
        attribute,
        default,
    )


def _language_payload(language: Any) -> dict[str, Any]:
    """
    Convert the internal language object into a stable API shape.
    """

    code = str(
        _safe_language_value(
            language,
            "code",
            "",
        )
    ).strip().lower()

    rtl = bool(
        _safe_language_value(
            language,
            "rtl",
            False,
        )
    )

    return {
        "code": code,
        "name": _safe_language_value(
            language,
            "name",
            code,
        ),
        "native_name": _safe_language_value(
            language,
            "native_name",
            _safe_language_value(
                language,
                "name",
                code,
            ),
        ),
        "locale": _safe_language_value(
            language,
            "locale",
            code,
        ),
        "rtl": rtl,
        "direction": "rtl" if rtl else "ltr",
        "ui_catalog_available": code in UI_CATALOG,
    }


def _safe_provider_summary() -> Any:
    """
    Get provider information without allowing provider
    introspection failures to break the i18n API.
    """

    try:
        summary_method = getattr(
            provider_manager,
            "summary",
            None,
        )

        if not callable(summary_method):
            return []

        return summary_method()

    except Exception as exc:
        return {
            "status": "unavailable",
            "error": str(exc),
        }


# =========================================================
# LANGUAGES
# =========================================================

@router.get("/languages")
def languages():
    """
    Return all languages registered in ACOS.
    """

    supported_languages = get_supported_languages()

    return {
        "status": "ok",
        "count": get_language_count(),
        "languages": [
            _language_payload(language)
            for language in supported_languages
        ],
    }


# =========================================================
# LANGUAGE DETAILS
# =========================================================

@router.get("/languages/{language_code}")
def language_details(
    language_code: str,
):
    """
    Return detailed information about one language.
    """

    language = _find_language(
        language_code
    )

    return {
        "status": "ok",
        "language": _language_payload(language),
    }


# =========================================================
# UI TRANSLATIONS
# =========================================================

@router.get("/ui/{language_code}")
def ui_translations(
    language_code: str,
):
    """
    Return ACOS UI translations.

    Languages without a dedicated catalog receive
    the English catalog as a temporary fallback.
    """

    language = _find_language(
        language_code
    )

    code = _normalize_language_code(
        _safe_language_value(
            language,
            "code",
            language_code,
        )
    )

    translations = UI_CATALOG.get(code)

    fallback = False

    if translations is None:
        translations = UI_CATALOG["en"].copy()
        fallback = True

    language_data = _language_payload(
        language
    )

    return {
        "status": "ok",
        "language": language_data,
        "fallback": fallback,
        "translations": translations,
    }


# =========================================================
# SINGLE UI TEXT
# =========================================================

@router.get("/text/{language_code}/{key}")
def ui_text(
    language_code: str,
    key: str,
):
    """
    Return one UI translation by key.
    """

    language = _find_language(
        language_code
    )

    code = _normalize_language_code(
        _safe_language_value(
            language,
            "code",
            language_code,
        )
    )

    catalog = UI_CATALOG.get(
        code,
        UI_CATALOG["en"],
    )

    value = catalog.get(
        key,
        UI_CATALOG["en"].get(
            key,
            key,
        ),
    )

    return {
        "status": "ok",
        "language": code,
        "key": key,
        "text": value,
    }


# =========================================================
# VALIDATION
# =========================================================

@router.get("/validate")
def validate():
    """
    Validate the existing ACOS translation system.
    """

    try:
        result = validate_translation_structure()

        return {
            "status": "ok",
            "valid": True,
            "validation": result,
            "languages": {
                "count": get_language_count(),
            },
            "ui_catalog": {
                "languages": sorted(
                    UI_CATALOG.keys()
                ),
                "count": len(UI_CATALOG),
            },
        }

    except Exception as exc:
        return {
            "status": "error",
            "valid": False,
            "validation": {
                "error": str(exc),
            },
            "languages": {
                "count": get_language_count(),
            },
            "ui_catalog": {
                "languages": sorted(
                    UI_CATALOG.keys()
                ),
                "count": len(UI_CATALOG),
            },
        }


# =========================================================
# PROVIDERS
# =========================================================

@router.get("/providers")
def providers():
    """
    Return the registered translation providers.
    """

    summary = _safe_provider_summary()

    return {
        "status": "ok",
        "providers": summary,
    }


# =========================================================
# TRANSLATION
# =========================================================

@router.post("/translate")
async def translate(
    request: TranslationRequest,
):
    """
    Translate text through the existing ACOS quality
    orchestrator.

    The orchestrator remains responsible for:
        - provider selection
        - provider execution
        - comparison
        - confidence
        - disagreement detection
        - final translation result
    """

    source_language = _normalize_language_code(
        request.source_language
    )

    target_language = _normalize_language_code(
        request.target_language
    )

    # -----------------------------------------------------
    # TARGET MUST ALWAYS BE KNOWN
    # -----------------------------------------------------

    _find_language(
        target_language
    )

    # -----------------------------------------------------
    # SOURCE
    # -----------------------------------------------------

    if source_language != "auto":
        _find_language(
            source_language
        )

    # -----------------------------------------------------
    # SAME LANGUAGE
    # -----------------------------------------------------

    if (
        source_language != "auto"
        and source_language == target_language
    ):
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
                "reason": (
                    "source_and_target_languages_are_identical"
                ),
            },
        }

    # -----------------------------------------------------
    # ORCHESTRATOR
    # -----------------------------------------------------

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
                "error": "translation_failed",
                "message": "Translation failed.",
                "reason": str(exc),
            },
        ) from exc

    # -----------------------------------------------------
    # NORMALIZED RESULT
    # -----------------------------------------------------

    return {
        "status": getattr(
            result,
            "status",
            "unknown",
        ),
        "source_language": source_language,
        "target_language": target_language,
        "source_text": request.text,
        "translation": getattr(
            result,
            "value",
            None,
        ),
        "confidence": getattr(
            result,
            "confidence",
            0.0,
        ),
        "providers_used": getattr(
            result,
            "providers_used",
            [],
        ),
        "successful_providers": getattr(
            result,
            "successful_providers",
            [],
        ),
        "failed_providers": getattr(
            result,
            "failed_providers",
            [],
        ),
        "unsupported_providers": getattr(
            result,
            "unsupported_providers",
            [],
        ),
        "disagreement": getattr(
            result,
            "disagreement",
            False,
        ),
        "details": getattr(
            result,
            "details",
            {},
        ),
    }


# =========================================================
# HEALTH
# =========================================================

@router.get("/health")
def health():
    """
    Lightweight health endpoint for Render and monitoring.
    """

    try:
        language_count = get_language_count()

        return {
            "status": "ok",
            "service": "ACOS Internationalization",
            "languages": language_count,
            "ui_catalog_languages": len(
                UI_CATALOG
            ),
            "ui_catalog": sorted(
                UI_CATALOG.keys()
            ),
            "providers": _safe_provider_summary(),
        }

    except Exception as exc:
        return {
            "status": "degraded",
            "service": "ACOS Internationalization",
            "error": str(exc),
        }
