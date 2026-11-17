from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ACOS"
    app_description: str = "AI Creative Operating System"
    version: str = "0.1.0"

    environment: str = "development"
    debug: bool = False

    database_url: str = "sqlite:///./acos.db"

    model_selection_mode: str = "quality_first"
    prefer_free_models: bool = True

    max_upload_size_mb: int = 2048

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
