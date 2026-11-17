from __future__ import annotations

import os


class SEOSettings:
    """
    Global ACOS SEO configuration.

    The same SEO system can be reused by
    every ACOS website/domain.
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

        self.robots_enabled = (
            os.getenv(
                "SEO_ROBOTS_ENABLED",
                "true",
            )
            .strip()
            .lower()
            in {
                "1",
                "true",
                "yes",
                "on",
            }
        )

        self.indexing_enabled = (
            os.getenv(
                "SEO_INDEXING_ENABLED",
                "true",
            )
            .strip()
            .lower()
            in {
                "1",
                "true",
                "yes",
                "on",
            }
        )


seo_settings = SEOSettings()
