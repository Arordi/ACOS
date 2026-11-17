from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageCapabilities:
    language_code: str

    translation: bool = False
    dictionary: bool = False
    grammar: bool = False
    spelling: bool = False
    semantic_check: bool = False

    text_to_speech: bool = False
    speech_to_text: bool = False
    pronunciation_assessment: bool = False

    phoneme_check: bool = False
    stress_check: bool = False
    prosody_check: bool = False


LANGUAGE_CAPABILITIES = {
    "en": LanguageCapabilities(
        language_code="en",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
        phoneme_check=True,
        stress_check=True,
        prosody_check=True,
    ),

    "hy": LanguageCapabilities(
        language_code="hy",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "zh": LanguageCapabilities(
        language_code="zh",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
        phoneme_check=True,
    ),

    "yue": LanguageCapabilities(
        language_code="yue",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "hi": LanguageCapabilities(
        language_code="hi",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "es": LanguageCapabilities(
        language_code="es",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "ar": LanguageCapabilities(
        language_code="ar",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "fr": LanguageCapabilities(
        language_code="fr",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "bn": LanguageCapabilities(
        language_code="bn",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "pt": LanguageCapabilities(
        language_code="pt",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "id": LanguageCapabilities(
        language_code="id",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "ur": LanguageCapabilities(
        language_code="ur",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "ru": LanguageCapabilities(
        language_code="ru",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "de": LanguageCapabilities(
        language_code="de",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "ja": LanguageCapabilities(
        language_code="ja",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "mr": LanguageCapabilities(
        language_code="mr",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "vi": LanguageCapabilities(
        language_code="vi",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "te": LanguageCapabilities(
        language_code="te",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "tr": LanguageCapabilities(
        language_code="tr",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "ta": LanguageCapabilities(
        language_code="ta",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "ko": LanguageCapabilities(
        language_code="ko",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "fa": LanguageCapabilities(
        language_code="fa",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "it": LanguageCapabilities(
        language_code="it",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
        pronunciation_assessment=True,
    ),

    "th": LanguageCapabilities(
        language_code="th",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "tl": LanguageCapabilities(
        language_code="tl",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "ha": LanguageCapabilities(
        language_code="ha",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "sw": LanguageCapabilities(
        language_code="sw",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "gu": LanguageCapabilities(
        language_code="gu",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "kn": LanguageCapabilities(
        language_code="kn",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),

    "pa": LanguageCapabilities(
        language_code="pa",
        translation=True,
        dictionary=True,
        grammar=True,
        spelling=True,
        semantic_check=True,
        text_to_speech=True,
        speech_to_text=True,
    ),
}


def get_capabilities(
    language_code: str,
) -> LanguageCapabilities | None:
    return LANGUAGE_CAPABILITIES.get(
        language_code
    )


def supports(
    language_code: str,
    capability: str,
) -> bool:
    capabilities = get_capabilities(
        language_code
    )

    if capabilities is None:
        return False

    return bool(
        getattr(
            capabilities,
            capability,
            False,
        )
    )
