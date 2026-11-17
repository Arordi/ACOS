import json
from pathlib import Path

from i18n.languages import get_language


TRANSLATIONS_DIR = Path(__file__).parent / "translations"


class TranslationManager:

    def __init__(self):
        self._cache: dict[str, dict[str, str]] = {}

    def load(self, language_code: str) -> dict[str, str]:
        language = get_language(language_code)

        if language.code in self._cache:
            return self._cache[language.code]

        path = TRANSLATIONS_DIR / f"{language.code}.json"

        if not path.exists():
            if language.code != "en":
                return self.load("en")

            raise FileNotFoundError(
                f"Missing translation file: {path}"
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError(
                f"Translation file must contain an object: {path}"
            )

        self._cache[language.code] = data

        return data

    def get(
        self,
        key: str,
        language_code: str = "en",
        default: str | None = None,
    ) -> str:

        translations = self.load(language_code)

        if key in translations:
            return translations[key]

        if language_code != "en":
            english = self.load("en")

            if key in english:
                return english[key]

        if default is not None:
            return default

        return key


translation_manager = TranslationManager()


def translate(
    key: str,
    language_code: str = "en",
    default: str | None = None,
) -> str:
    return translation_manager.get(
        key=key,
        language_code=language_code,
        default=default,
    )
