from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PageMetadata:
    title: str
    description: str

    canonical_url: str

    language: str = "en"

    robots: str = (
        "index, follow"
    )

    image_url: str | None = None

    site_name: str = "ACOS"

    type: str = "website"


class MetadataManager:

    def __init__(self):
        self._pages: dict[
            str,
            PageMetadata,
        ] = {}

    def register(
        self,
        path: str,
        metadata: PageMetadata,
    ) -> None:

        normalized_path = (
            path
            if path.startswith("/")
            else f"/{path}"
        )

        self._pages[
            normalized_path
        ] = metadata

    def get(
        self,
        path: str,
    ) -> PageMetadata | None:

        return self._pages.get(
            path
        )

    def all(
        self,
    ) -> dict[str, PageMetadata]:

        return dict(self._pages)

    def remove(
        self,
        path: str,
    ) -> None:

        self._pages.pop(
            path,
            None,
        )


metadata_manager = MetadataManager()
