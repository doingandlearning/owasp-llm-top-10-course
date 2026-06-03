class LLMError(Exception):
    """Base error for LLM provider calls."""


class LLMNotConfigured(LLMError):
    """Live mode selected but API credentials are missing."""


class LLMDisabled(LLMError):
    """Live LLM blocked by DISABLE_LIVE_LLM."""


class LLMProviderError(LLMError):
    """Upstream model API returned an error."""
