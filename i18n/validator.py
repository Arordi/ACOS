import json
from pathlib import Path

from i18n.languages import SUPPORTED_LANGUAGES


TRANSLATIONS_DIR = Path(__file__).parent / "translations"


def load_translation(language_code: str) -> dict:
    path = TRANSLATIONS_DIR / f"{language_code}.json"

    if not path.exists():
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

    return data


def validate_translation_structure() -> dict:
    errors = []
    warnings = []

    primary = load_translation("en")
    primary_keys = set(primary.keys())

    for language in SUPPORTED_LANGUAGES:

        try:
            translations = load_translation(
                language.code
            )

        except (FileNotFoundError, ValueError) as exc:
            warnings.append(str(exc))
            continue

        translation_keys = set(
            translations.keys()
        )

        missing_keys = (
            primary_keys - translation_keys
        )

        extra_keys = (
            translation_keys - primary_keys
        )

        for key in sorted(missing_keys):
            errors.append(
                f"[{language.code}] "
                f"Missing key: {key}"
            )

        for key in sorted(extra_keys):
            warnings.append(
                f"[{language.code}] "
                f"Extra key: {key}"
            )

        for key, value in translations.items():

            if not isinstance(value, str):
                errors.append(
                    f"[{language.code}] "
                    f"Value must be string: {key}"
                )

            elif not value.strip():
                errors.append(
                    f"[{language.code}] "
                    f"Empty translation: {key}"
                )

    return {
        "errors": errors,
        "warnings": warnings,
        "valid": len(errors) == 0,
    }
