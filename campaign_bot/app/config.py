import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def resolve_root() -> Path:
    """
    Project root containing static/, templates/, data/, etc.
    Editable installs use campaign_bot/; pip installs bundle assets beside app/;
    Docker sets CAMPAIGN_BOT_ROOT=/app.
    """
    override = os.getenv("CAMPAIGN_BOT_ROOT")
    if override:
        root = Path(override).resolve()
    else:
        root = Path(__file__).resolve().parent.parent

    if not (root / "static").is_dir() or not (root / "templates").is_dir():
        raise RuntimeError(
            f"CampaignBot assets not found under {root}. "
            "Set CAMPAIGN_BOT_ROOT to the directory that contains static/ and templates/."
        )
    return root


ROOT = resolve_root()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_mode: str = "stub"
    show_prompt: bool = True
    debug: bool = False
    disable_live_llm: bool = False
    host: str = "127.0.0.1"
    port: int = 8080

    # openai = /v1/chat/completions | anthropic = Claude Messages API
    llm_provider: str = "openai"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-haiku-4-5-20251001"
    anthropic_base_url: str = "https://api.anthropic.com"
    anthropic_api_version: str = "2023-06-01"
    anthropic_max_tokens: int = 1024
    llm_timeout_seconds: float = 60.0
    # lab = naive priority rules (workshop default) | hardened = explicit guardrails
    system_prompt_style: str = "lab"
    llm_temperature: float = 0.9

    def normalized_llm_mode(self) -> str:
        return self.llm_mode.strip().lower()

    def normalized_llm_provider(self) -> str:
        return self.llm_provider.strip().lower()

    def normalized_system_prompt_style(self) -> str:
        return self.system_prompt_style.strip().lower()

    def live_ready(self) -> bool:
        if self.disable_live_llm:
            return False
        if self.normalized_llm_provider() == "anthropic":
            return bool(self.anthropic_api_key)
        return bool(self.openai_api_key)

    def live_model_name(self) -> str:
        if self.normalized_llm_provider() == "anthropic":
            return self.anthropic_model
        return self.openai_model

    def live_config_hint(self) -> str:
        if self.normalized_llm_provider() == "anthropic":
            return "ANTHROPIC_API_KEY not configured"
        return "OPENAI_API_KEY not configured"

    @property
    def data_dir(self) -> Path:
        return ROOT / "data"

    @property
    def prompts_dir(self) -> Path:
        return ROOT / "prompts"


settings = Settings()
