from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    code: str
    name: str
    native_name: str
    locale: str
    rtl: bool = False


# ============================================================
# ACOS — Supported Languages
#
# IMPORTANT:
# 1. English is the primary language.
# 2. Armenian is immediately after English.
# 3. Total supported languages: 30
# ============================================================

SUPPORTED_LANGUAGES = [

    # 1
    Language(
        code="en",
        name="English",
        native_name="English",
        locale="en-US",
    ),

    # 2
    Language(
        code="hy",
        name="Armenian",
        native_name="Հայերեն",
        locale="hy-AM",
    ),

    # 3
    Language(
        code="zh",
        name="Chinese",
        native_name="中文",
        locale="zh-CN",
    ),

    # 4
    Language(
        code="hi",
        name="Hindi",
        native_name="हिन्दी",
        locale="hi-IN",
    ),

    # 5
    Language(
        code="es",
        name="Spanish",
        native_name="Español",
        locale="es-ES",
    ),

    # 6
    Language(
        code="ar",
        name="Arabic",
        native_name="العربية",
        locale="ar-SA",
        rtl=True,
    ),

    # 7
    Language(
        code="fr",
        name="French",
        native_name="Français",
        locale="fr-FR",
    ),

    # 8
    Language(
        code="bn",
        name="Bengali",
        native_name="বাংলা",
        locale="bn-BD",
    ),

    # 9
    Language(
        code="pt",
        name="Portuguese",
        native_name="Português",
        locale="pt-BR",
    ),

    # 10
    Language(
        code="id",
        name="Indonesian",
        native_name="Bahasa Indonesia",
        locale="id-ID",
    ),

    # 11
    Language(
        code="ur",
        name="Urdu",
        native_name="اردو",
        locale="ur-PK",
        rtl=True,
    ),

    # 12
    Language(
        code="ru",
        name="Russian",
        native_name="Русский",
        locale="ru-RU",
    ),

    # 13
    Language(
        code="de",
        name="German",
        native_name="Deutsch",
        locale="de-DE",
    ),

    # 14
    Language(
        code="ja",
        name="Japanese",
        native_name="日本語",
        locale="ja-JP",
    ),

    # 15
    Language(
        code="mr",
        name="Marathi",
        native_name="मराठी",
        locale="mr-IN",
    ),

    # 16
    Language(
        code="vi",
        name="Vietnamese",
        native_name="Tiếng Việt",
        locale="vi-VN",
    ),

    # 17
    Language(
        code="te",
        name="Telugu",
        native_name="తెలుగు",
        locale="te-IN",
    ),

    # 18
    Language(
        code="tr",
        name="Turkish",
        native_name="Türkçe",
        locale="tr-TR",
    ),

    # 19
    Language(
        code="ta",
        name="Tamil",
        native_name="தமிழ்",
        locale="ta-IN",
    ),

    # 20
    Language(
        code="ko",
        name="Korean",
        native_name="한국어",
        locale="ko-KR",
    ),

    # 21
    Language(
        code="fa",
        name="Persian",
        native_name="فارسی",
        locale="fa-IR",
        rtl=True,
    ),

    # 22
    Language(
        code="it",
        name="Italian",
        native_name="Italiano",
        locale="it-IT",
    ),

    # 23
    Language(
        code="th",
        name="Thai",
        native_name="ไทย",
        locale="th-TH",
    ),

    # 24
    Language(
        code="tl",
        name="Tagalog / Filipino",
        native_name="Tagalog / Filipino",
        locale="fil-PH",
    ),

    # 25
    Language(
        code="ha",
        name="Hausa",
        native_name="Hausa",
        locale="ha-NG",
    ),

    # 26
    Language(
        code="sw",
        name="Swahili",
        native_name="Kiswahili",
        locale="sw-KE",
    ),

    # 27
    Language(
        code="yue",
        name="Cantonese",
        native_name="廣東話",
        locale="zh-HK",
    ),

    # 28
    Language(
        code="gu",
        name="Gujarati",
        native_name="ગુજરાતી",
        locale="gu-IN",
    ),

    # 29
    Language(
        code="kn",
        name="Kannada",
        native_name="ಕನ್ನಡ",
        locale="kn-IN",
    ),

    # 30
    Language(
        code="pa",
        name="Punjabi",
        native_name="ਪੰਜਾਬੀ",
        locale="pa-IN",
    ),
]


# ============================================================
# Fast lookup
# ============================================================

LANGUAGE_MAP = {
    language.code: language
    for language in SUPPORTED_LANGUAGES
}


# ============================================================
# Language helpers
# ============================================================

def get_language(code: str) -> Language:
    """
    Return the requested language.

    If the language does not exist,
    English is used as the safe fallback.
    """
    return LANGUAGE_MAP.get(
        code,
        LANGUAGE_MAP["en"],
    )


def get_supported_languages() -> list[Language]:
    """
    Return all 30 ACOS supported languages
    in the official ACOS order.
    """
    return SUPPORTED_LANGUAGES


def is_supported_language(code: str) -> bool:
    """
    Check whether a language is supported.
    """
    return code in LANGUAGE_MAP


def get_language_count() -> int:
    """
    Return the total number of supported languages.
    """
    return len(SUPPORTED_LANGUAGES)


def is_rtl_language(code: str) -> bool:
    """
    Check whether a language uses
    right-to-left text direction.
    """
    language = get_language(code)
    return language.rtl
