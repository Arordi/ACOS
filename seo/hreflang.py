from __future__ import annotations

from i18n.languages import (
    get_supported_languages,
)
from seo.config import seo_settings


def generate_hreflang(
    path: str = "/",
) -> list[dict[str, str]]:

    normalized_path = (
        path
        if path.startswith("/")
        else f"/{path}"
    )

    result = []

    for language in (
        get_supported_languages()
    ):

        result.append(
            {
                "hreflang":
                    language.locale,
                "language":
                    language.code,
                "url":
                    (
                        f"{seo_settings.base_url}"
                        f"{normalized_path}"
                        f"?lang={language.code}"
                    ),
            }
        )

    result.append(
        {
            "hreflang": "x-default",
            "language": (
                seo_settings
                .default_language
            ),
            "url": (
                f"{seo_settings.base_url}"
                f"{normalized_path}"
            ),
        }
    )

    return result
