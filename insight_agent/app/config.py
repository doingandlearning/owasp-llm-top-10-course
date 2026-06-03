import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def resolve_root() -> Path:
    override = os.getenv("INSIGHT_AGENT_ROOT")
    if override:
        root = Path(override).resolve()
    else:
        root = Path(__file__).resolve().parent.parent

    if not (root / "static").is_dir() or not (root / "templates").is_dir():
        raise RuntimeError(
            f"InsightAgent assets not found under {root}. "
            "Set INSIGHT_AGENT_ROOT to the directory with static/ and templates/."
        )
    return root


ROOT = resolve_root()


def resolve_data_dir(root: Path) -> Path:
    override = os.getenv("LAB_DATA_DIR")
    if override:
        return Path(override).resolve()
    shared = root.parent / "data"
    if (shared / "customers.json").is_file():
        return shared
    return root / "data"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_mode: str = "stub"
    system_prompt_style: str = "lab"
    show_prompt: bool = True
    debug: bool = False
    disable_live_llm: bool = False
    host: str = "127.0.0.1"
    port: int = 8081
    max_tool_steps: int = 5

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
        return resolve_data_dir(ROOT)

    @property
    def prompts_dir(self) -> Path:
        return ROOT / "prompts"

    @property
    def payloads_dir(self) -> Path:
        return ROOT / "payloads"

    @property
    def exports_dir(self) -> Path:
        path = ROOT / "exports"
        path.mkdir(exist_ok=True)
        return path

    @property
    def sends_log(self) -> Path:
        return ROOT / "sends.jsonl"


settings = Settings()
