from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ProviderSettings:
    name: str
    enabled: bool
    api_key: str | None
    endpoint: str | None


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


def get_provider_settings(
    name: str,
) -> ProviderSettings:

    prefix = name.upper().replace(
        "-",
        "_",
    )

    return ProviderSettings(
        name=name,
        enabled=_env_bool(
            f"{prefix}_ENABLED",
            False,
        ),
        api_key=os.getenv(
            f"{prefix}_API_KEY"
        ),
        endpoint=os.getenv(
            f"{prefix}_ENDPOINT"
        ),
    )


class I18nSettings:

    def __init__(self):

        self.mode = os.getenv(
            "I18N_PROVIDER_MODE",
            "quality_first",
        )

        self.max_concurrency = int(
            os.getenv(
                "I18N_MAX_CONCURRENCY",
                "10",
            )
        )

        self.min_confidence = float(
            os.getenv(
                "I18N_MIN_CONFIDENCE",
                "85",
            )
        )

        self.review_threshold = float(
            os.getenv(
                "I18N_REVIEW_THRESHOLD",
                "85",
            )
        )

        self.pass_threshold = float(
            os.getenv(
                "I18N_PASS_THRESHOLD",
                "95",
            )
        )

        self.providers = {}


settings = I18nSettings()
