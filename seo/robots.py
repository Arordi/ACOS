from __future__ import annotations

from seo.config import seo_settings


def generate_robots() -> str:

    if not seo_settings.robots_enabled:
        return (
            "User-agent: *\n"
            "Disallow: /\n"
        )

    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "Disallow: /api/",
        "Disallow: /docs",
        "Disallow: /redoc",
        "Disallow: /openapi.json",
        "",
        (
            "Sitemap: "
            f"{seo_settings.base_url}"
            "/sitemap.xml"
        ),
    ]

    if not seo_settings.indexing_enabled:
        lines.extend([
            "",
            "# Indexing is disabled by configuration.",
        ])

    return "\n".join(lines) + "\n"
