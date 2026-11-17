from __future__ import annotations

import json

from seo.config import seo_settings


def generate_website_schema() -> dict:

    return {
        "@context":
            "https://schema.org",

        "@type":
            "WebApplication",

        "name":
            seo_settings.site_name,

        "description":
            seo_settings.site_description,

        "url":
            seo_settings.base_url,

        "applicationCategory":
            "MultimediaApplication",

        "operatingSystem":
            "Web",

        "inLanguage":
            "en",

        "browserRequirements":
            "Requires JavaScript",
    }


def generate_json_ld() -> str:

    return json.dumps(
        generate_website_schema(),
        ensure_ascii=False,
        separators=(
            ",",
            ":",
        ),
    )
