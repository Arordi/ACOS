from __future__ import annotations

import os


def _env_bool(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


class SEOSettings:
    """
    Central SEO configuration for ACOS.

    The configuration is environment-based so the same
    SEO system can be reused for different websites
    and domains.
    """

    def __init__(self):
        self.site_name = os.getenv(
            "SEO_SITE_NAME",
            "ACOS",
        )

        self.site_description = os.getenv(
            "SEO_SITE_DESCRIPTION",
            "AI Creative Operating System",
        )

        self.base_url = os.getenv(
            "SEO_BASE_URL",
            "https://acos.onrender.com",
        ).rstrip("/")

        self.default_language = os.getenv(
            "SEO_DEFAULT_LANGUAGE",
            "en",
        )

        self.robots_enabled = _env_bool(
            "SEO_ROBOTS_ENABLED",
            True,
        )

        self.indexing_enabled = _env_bool(
            "SEO_INDEXING_ENABLED",
            True,
        )


seo_settings = SEOSettings()
