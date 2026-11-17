from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import (
    PlainTextResponse,
    Response,
)

from seo.hreflang import (
    generate_hreflang,
)
from seo.metadata import (
    metadata_manager,
)
from seo.robots import (
    generate_robots,
)
from seo.sitemap import (
    generate_sitemap,
)
from seo.structured_data import (
    generate_website_schema,
)


router = APIRouter(
    tags=["SEO"],
)


@router.get(
    "/robots.txt",
    response_class=PlainTextResponse,
    include_in_schema=False,
)
def robots():
    return generate_robots()


@router.get(
    "/sitemap.xml",
    include_in_schema=False,
)
def sitemap():

    return Response(
        content=generate_sitemap(),
        media_type="application/xml",
    )


@router.get(
    "/api/seo/status",
)
def seo_status():

    return {
        "status": "ok",
        "seo": {
            "robots": True,
            "sitemap": True,
            "structured_data": True,
            "hreflang": True,
        },
        "registered_pages":
            len(
                metadata_manager.all()
            ),
    }


@router.get(
    "/api/seo/hreflang",
)
def hreflang():

    return {
        "links":
            generate_hreflang("/")
    }


@router.get(
    "/api/seo/structured-data",
)
def structured_data():

    return generate_website_schema()
