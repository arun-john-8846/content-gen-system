"""
LLM client abstraction for Content Gen Web.

Supports:
  - Anthropic (direct API via anthropic SDK)
  - OpenAI (direct API via openai SDK)
  - MCP proxy (routes via an MCP SSE server when USE_MCP_SERVER=true)

Usage:
    from llm_client import send, LLMError

    text = send(system="You are ...", user="Do X")
"""

import json
import time
import config


class LLMError(Exception):
    """Raised when an LLM call fails after all retries."""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _provider() -> str:
    return config.get("llm_provider").lower()


def _use_mcp() -> bool:
    return config.get("use_mcp_server").lower() == "true"


# ── Anthropic ─────────────────────────────────────────────────────────────────

def _send_anthropic(system: str, user: str, model: str) -> str:
    try:
        import anthropic
    except ImportError:
        raise LLMError("anthropic package not installed. Run: pip install anthropic")

    api_key = config.get("anthropic_api_key")
    if not api_key:
        raise LLMError(
            "Anthropic API key not set. Go to /settings and enter your ANTHROPIC_API_KEY."
        )

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=8192,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    # response.content is a list of ContentBlock objects
    parts = []
    for block in response.content:
        if hasattr(block, "text"):
            parts.append(block.text)
    return "".join(parts)


# ── OpenAI ────────────────────────────────────────────────────────────────────

def _send_openai(system: str, user: str, model: str) -> str:
    try:
        import openai
    except ImportError:
        raise LLMError("openai package not installed. Run: pip install openai")

    api_key = config.get("openai_api_key")
    if not api_key:
        raise LLMError(
            "OpenAI API key not set. Go to /settings and enter your OPENAI_API_KEY."
        )

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=8192,
    )
    return response.choices[0].message.content or ""


# ── MCP proxy ─────────────────────────────────────────────────────────────────

def _send_mcp(system: str, user: str, model: str) -> str:
    """Call the MCP server's llm_proxy tool via its SSE HTTP transport."""
    try:
        import requests
    except ImportError:
        raise LLMError("requests package not installed. Run: pip install requests")

    mcp_url = config.get("mcp_server_url").rstrip("/")
    if not mcp_url:
        raise LLMError(
            "MCP server URL not set. Go to /settings and enter the MCP_SERVER_URL."
        )

    # MCP JSON-RPC 2.0 call to the llm_proxy tool
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "llm_proxy",
            "arguments": {
                "system": system,
                "user": user,
                "model": model,
            },
        },
    }

    try:
        resp = requests.post(
            f"{mcp_url}/rpc",
            json=payload,
            timeout=300,  # LLM calls can be slow
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        raise LLMError(f"MCP server request failed: {exc}") from exc

    if "error" in data:
        raise LLMError(f"MCP server returned error: {data['error']}")

    # Extract text from MCP tool result
    result = data.get("result", {})
    content = result.get("content", [])
    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(item["text"])
    return "".join(parts)


# ── Public API ────────────────────────────────────────────────────────────────

def send(system: str, user: str, model=None, max_retries: int = 3) -> str:
    """
    Send a prompt to the configured LLM provider.

    Args:
        system:      System prompt text.
        user:        User message text.
        model:       Override model name. If None, uses the configured default.
        max_retries: Number of retry attempts on transient errors (default 3).

    Returns:
        The model's text response as a string.

    Raises:
        LLMError: On configuration errors or after all retries exhausted.
    """
    # Resolve model name
    if not model:
        if _use_mcp():
            # Let the MCP server decide based on its own config
            model = config.get("anthropic_model") or config.get("openai_model")
        elif _provider() == "openai":
            model = config.get("openai_model") or "gpt-4o"
        else:
            model = config.get("anthropic_model") or "claude-sonnet-4-5-20251022"

    last_err: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            if _use_mcp():
                return _send_mcp(system, user, model)
            elif _provider() == "openai":
                return _send_openai(system, user, model)
            else:
                return _send_anthropic(system, user, model)
        except LLMError:
            raise  # config errors are not retryable
        except Exception as exc:
            last_err = exc
            if attempt < max_retries:
                wait = 4 * attempt  # 4s, 8s
                time.sleep(wait)

    raise LLMError(
        f"LLM call failed after {max_retries} attempts: {last_err}"
    ) from last_err
