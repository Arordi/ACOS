from __future__ import annotations

from datetime import datetime, timezone
from xml.etree.ElementTree import (
    Element,
    SubElement,
    tostring,
)

from seo.config import seo_settings
from seo.metadata import metadata_manager


SITEMAP_NAMESPACE = (
    "http://www.sitemaps.org/schemas/sitemap/0.9"
)


def generate_sitemap() -> str:

    urlset = Element(
        "urlset",
        {
            "xmlns":
                SITEMAP_NAMESPACE,
        },
    )

    pages = metadata_manager.all()

    if not pages:
        default_pages = [
            "/",
        ]

        for path in default_pages:
            url = SubElement(
                urlset,
                "url",
            )

            loc = SubElement(
                url,
                "loc",
            )

            loc.text = (
                f"{seo_settings.base_url}"
                f"{path}"
            )

            lastmod = SubElement(
                url,
                "lastmod",
            )

            lastmod.text = (
                datetime.now(
                    timezone.utc
                )
                .date()
                .isoformat()
            )

    else:
        for path, metadata in pages.items():

            if (
                metadata.robots
                .lower()
                .startswith("noindex")
            ):
                continue

            url = SubElement(
                urlset,
                "url",
            )

            loc = SubElement(
                url,
                "loc",
            )

            loc.text = metadata.canonical_url

            lastmod = SubElement(
                url,
                "lastmod",
            )

            lastmod.text = (
                datetime.now(
                    timezone.utc
                )
                .date()
                .isoformat()
            )

    xml = tostring(
        urlset,
        encoding="unicode",
    )

    return (
        '<?xml version="1.0" '
        'encoding="UTF-8"?>\n'
        + xml
    )
