from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_mode: str = "stub"
    show_prompt: bool = True
    host: str = "127.0.0.1"
    port: int = 8080

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    @property
    def data_dir(self) -> Path:
        return ROOT / "data"

    @property
    def prompts_dir(self) -> Path:
        return ROOT / "prompts"


settings = Settings()
