"""
MCP server for ADAP Content Gen Web.

Exposes two tools:
  - llm_proxy(system, user, model)  — proxies an LLM call to the configured provider
  - run_pipeline(slug)              — runs the full auto pipeline for a page slug

Usage:
  # stdio mode (Claude Desktop, Cursor, etc.)
  python mcp_server.py

  # SSE HTTP mode (web app routing via USE_MCP_SERVER=true)
  python mcp_server.py --sse [--port 8090]

Claude Desktop config (~/.claude_desktop_config.json):
  {
    "mcpServers": {
      "adap": {
        "command": "python",
        "args": ["/path/to/ADAP-Content-Gen-Web/mcp_server.py"],
        "env": {
          "ANTHROPIC_API_KEY": "sk-ant-...",
          "LLM_PROVIDER": "anthropic"
        }
      }
    }
  }
"""

import argparse
import os
import sys
from pathlib import Path

# Ensure the project root is on the Python path so we can import pipeline etc.
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load .env if present (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass

import models
import config
import llm_client
import pipeline as _pipeline


# ── MCP tool implementations ──────────────────────────────────────────────────

def tool_llm_proxy(system: str, user: str, model=None) -> str:
    """Proxy an LLM call to the configured provider. Returns the model's text response."""
    return llm_client.send(system, user, model=model or None)


def tool_run_pipeline(slug: str) -> str:
    """
    Run the full auto pipeline (brief → draft → humanize+QA → deliver) for a page slug.
    Blocks until complete. Returns a status message.
    """
    page = models.get_page(slug)
    if not page:
        return f'Error: page "{slug}" not found in database.'

    if _pipeline.is_running(slug):
        return f'Pipeline is already running for "{slug}".'

    log_lines: list[str] = []

    import threading
    done_event = threading.Event()

    def _log(msg: str) -> None:
        log_lines.append(msg)

    def _run() -> None:
        try:
            _pipeline.run_auto_pipeline(slug, _log, threading.Event())
        except Exception as exc:
            _log(f"Pipeline error: {exc}")
        finally:
            done_event.set()

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    done_event.wait()  # block until pipeline finishes

    last_line = log_lines[-1] if log_lines else "No output."
    return f"Pipeline finished for \"{slug}\". Last log: {last_line}"


# ── MCP server bootstrap ──────────────────────────────────────────────────────

def build_mcp_server():
    """Build and return the MCP server instance."""
    try:
        from mcp.server import Server
        from mcp.server.models import InitializationOptions
        from mcp import types
    except ImportError:
        print(
            "ERROR: 'mcp' package not installed.\n"
            "Install it with: pip install mcp",
            file=sys.stderr,
        )
        sys.exit(1)

    server = Server("adap-content-gen")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="llm_proxy",
                description=(
                    "Send a prompt to the configured LLM provider (Anthropic or OpenAI) "
                    "and return the response text."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "system": {"type": "string", "description": "System prompt"},
                        "user":   {"type": "string", "description": "User message"},
                        "model":  {"type": "string", "description": "Model override (optional)"},
                    },
                    "required": ["system", "user"],
                },
            ),
            types.Tool(
                name="run_pipeline",
                description=(
                    "Run the full content generation pipeline for an ADAudit Plus feature page. "
                    "Steps: brief → draft → humanize+QA → delivery. Blocks until complete."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slug": {
                            "type": "string",
                            "description": "Page slug (e.g. 'active-directory-auditing')",
                        }
                    },
                    "required": ["slug"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        if name == "llm_proxy":
            system = arguments.get("system", "")
            user = arguments.get("user", "")
            model = arguments.get("model")
            try:
                result = tool_llm_proxy(system, user, model)
                return [types.TextContent(type="text", text=result)]
            except llm_client.LLMError as exc:
                return [types.TextContent(type="text", text=f"LLM error: {exc}")]

        elif name == "run_pipeline":
            slug = arguments.get("slug", "")
            result = tool_run_pipeline(slug)
            return [types.TextContent(type="text", text=result)]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    return server


# ── Entry points ──────────────────────────────────────────────────────────────

def run_stdio():
    """Run the MCP server in stdio mode (for Claude Desktop / Cursor)."""
    import asyncio
    from mcp.server.stdio import stdio_server

    async def _main():
        models.init_db()
        server = build_mcp_server()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )

    asyncio.run(_main())


def run_sse(port: int = 8090):
    """Run the MCP server in SSE/HTTP mode (for web app integration)."""
    import asyncio
    try:
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        import uvicorn
    except ImportError:
        print(
            "ERROR: SSE mode requires additional packages.\n"
            "Install them with: pip install mcp[sse] uvicorn starlette",
            file=sys.stderr,
        )
        sys.exit(1)

    models.init_db()
    server = build_mcp_server()
    sse = SseServerTransport("/messages")

    async def handle_sse(request):
        async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
            await server.run(streams[0], streams[1], server.create_initialization_options())

    async def handle_messages(request):
        await sse.handle_post_message(request.scope, request.receive, request._send)

    starlette_app = Starlette(
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages", app=handle_messages),
        ]
    )

    print(f"ADAP MCP server (SSE mode) starting on http://0.0.0.0:{port}")
    print(f"  SSE endpoint:  http://localhost:{port}/sse")
    print(f"  Set MCP_SERVER_URL=http://localhost:{port} in the web app settings.")
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ADAP MCP server")
    parser.add_argument("--sse", action="store_true", help="Run in SSE/HTTP mode")
    parser.add_argument("--port", type=int, default=8090, help="Port for SSE mode (default: 8090)")
    args = parser.parse_args()

    if args.sse:
        run_sse(port=args.port)
    else:
        run_stdio()
