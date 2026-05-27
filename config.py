"""
Configuration loader for Content Gen Web.

Priority order:
  1. Environment variables (set by Fly.io secrets or local .env loaded at startup)
  2. DB settings table (editable via the /settings web page)
  3. Hardcoded defaults

Environment variables take precedence so that cloud deployments using
`flyctl secrets set` work without touching the database.
"""

import os
import models


# Keys expected in settings
KNOWN_KEYS = {
    "llm_provider",       # "anthropic" | "openai"
    "anthropic_api_key",
    "openai_api_key",
    "anthropic_model",    # default: claude-sonnet-4-5-20251022
    "openai_model",       # default: gpt-4o
    "use_mcp_server",     # "true" | "false"
    "mcp_server_url",     # e.g. http://localhost:8090/sse
}

# Map setting key → environment variable name
_ENV_MAP = {
    "llm_provider":       "LLM_PROVIDER",
    "anthropic_api_key":  "ANTHROPIC_API_KEY",
    "openai_api_key":     "OPENAI_API_KEY",
    "anthropic_model":    "ANTHROPIC_MODEL",
    "openai_model":       "OPENAI_MODEL",
    "use_mcp_server":     "USE_MCP_SERVER",
    "mcp_server_url":     "MCP_SERVER_URL",
}

_DEFAULTS = {
    "llm_provider":      "anthropic",
    "anthropic_model":   "claude-sonnet-4-5-20251022",
    "openai_model":      "gpt-4o",
    "use_mcp_server":    "false",
    "mcp_server_url":    "",
    "anthropic_api_key": "",
    "openai_api_key":    "",
}


def get(key: str) -> str:
    """Return the effective value for a config key."""
    # 1. Environment variable
    env_name = _ENV_MAP.get(key)
    if env_name:
        env_val = os.environ.get(env_name)
        if env_val is not None:
            return env_val
    # 2. DB setting
    db_val = models.get_setting(key)
    if db_val:
        return db_val
    # 3. Default
    return _DEFAULTS.get(key, "")


def set(key: str, value: str) -> None:
    """Persist a setting to the DB (does not affect environment variables)."""
    if key in KNOWN_KEYS:
        models.set_setting(key, value)


def get_all_for_ui() -> dict:
    """
    Return all settings for the settings page UI.
    Masks API key values so they are never sent to the browser in plaintext.
    Shows '(set via environment)' if the key comes from an env var.
    """
    result = {}
    for key in KNOWN_KEYS:
        env_name = _ENV_MAP.get(key)
        from_env = bool(env_name and os.environ.get(env_name))
        value = get(key)
        is_key_field = key.endswith("_api_key")
        if is_key_field and value:
            display = "(set via environment)" if from_env else "••••••••" + value[-4:]
        else:
            display = "(set via environment)" if from_env else value
        result[key] = {
            "value": display,
            "from_env": from_env,
            "editable": not from_env,
        }
    return result
