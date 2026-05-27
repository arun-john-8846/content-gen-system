# Content Gen Web

A platform-agnostic web app for running a multi-step content production pipeline.
Runs standalone — no VS Code or IDE required.

## What it does

- **Dashboard** — tracks all pages through a 6-step workflow
- **Research** — triggers `serp_research.py` (SERP scraping via Playwright + Chrome)
- **LLM pipeline** — brief → draft → humanize+QA loop → delivery, fully automated
- **Settings** — configure API keys, pipeline prompt templates, and reference files via the web UI
- **MCP server** — optional; exposes `llm_proxy` and `run_pipeline` tools for Claude Desktop / Cursor
- **Delivery** — generates `_publish.docx` and `_review.docx`

---

## Quick start (local)

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers (needed for research only)
playwright install chromium

# 4. Set your API key
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY or OPENAI_API_KEY

# 5. Run the app
python app.py
# Open http://localhost:5001
```

Or via the convenience script:
```bash
./run.sh
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | — | Your Anthropic API key |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-5-20251022` | Anthropic model name |
| `OPENAI_API_KEY` | — | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI model name |
| `USE_MCP_SERVER` | `false` | Route LLM calls via MCP server |
| `MCP_SERVER_URL` | — | MCP server URL (e.g. `http://localhost:8090`) |
| `FLASK_SECRET_KEY` | `content-gen-web-2026` | Flask session secret — change in production |
| `DATABASE_PATH` | `./adap.db` | SQLite path — set to `/data/adap.db` on Fly.io |
| `PORT` | `5001` | Server port |

All variables can also be set via the **Settings** page (`/settings`).
Environment variables take priority over DB settings.

---

## MCP server

The MCP server exposes two tools for use with Claude Desktop, Cursor, or any MCP-compatible client.

### Stdio mode (Claude Desktop / Cursor)

```bash
python mcp_server.py
```

Claude Desktop config (`~/.claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "content-gen": {
      "command": "python",
      "args": ["/path/to/content-gen-web/mcp_server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "LLM_PROVIDER": "anthropic"
      }
    }
  }
}
```

### SSE/HTTP mode (web app integration)

```bash
python mcp_server.py --sse --port 8090
```

Then in the web app Settings, set:
- **Enable MCP**: Enabled
- **MCP server URL**: `http://localhost:8090`

### Available tools

| Tool | Description |
|---|---|
| `llm_proxy(system, user, model?)` | Send a prompt to the configured LLM provider |
| `run_pipeline(slug)` | Run the full pipeline for a page slug (blocking) |

---

## SERP research — local only

`serp_research.py` uses a real persistent Chrome profile logged into Google.
It **cannot run on Fly.io or any cloud server** — it requires:
- A local Chrome profile with Google sign-in
- A US-located network connection (or US VPN active)

**Workflow for cloud deploys:**
1. Run research locally: the app writes to `research/<keyword-slug>/`
2. Sync `research/` to the cloud volume (rsync, Fly.io volume transfer, etc.)
3. Run the LLM pipeline on the cloud app — it reads the research summaries and does not need Chrome

---

## Fly.io deployment

```bash
# Install flyctl if not already installed
brew install flyctl

# Authenticate
flyctl auth login

# Create the app (first time)
flyctl launch --no-deploy

# Create a persistent volume
flyctl volumes create adap_data --size 5 --region lax

# Set secrets
flyctl secrets set FLASK_SECRET_KEY="$(openssl rand -hex 32)"
flyctl secrets set ANTHROPIC_API_KEY="sk-ant-..."
flyctl secrets set LLM_PROVIDER="anthropic"

# Deploy
flyctl deploy

# View logs
flyctl logs
```

---

## Docker (local testing)

```bash
docker compose up --build
# Open http://localhost:5001
```

---

## Project structure

```
content-gen-web/
  app.py              Flask app (routes, views)
  pipeline.py         LLM pipeline (brief → draft → humanize+QA → deliver)
  llm_client.py       Anthropic/OpenAI/MCP abstraction
  mcp_server.py       MCP server (stdio + SSE modes)
  config.py           Settings loader (env → DB → defaults)
  models.py           SQLite schema + CRUD (pages, jobs, step_events, settings, prompts)
  jobs.py             Research subprocess runner
  requirements.txt
  .env.example
  Dockerfile
  fly.toml
  docker-compose.yml
  static/
    app.js            Research log polling + pipeline SSE
    style.css
  templates/
    base.html             Nav with Settings link
    dashboard.html
    new_page.html
    page_detail.html      6 tabs including Pipeline tab
    settings.html         API key / provider / MCP configuration
    settings_prompts.html Edit per-step LLM prompt templates
    settings_reference.html Upload / manage reference .md/.docx/.txt files
    research_view.html
  tools/              Python tools (serp_research.py, qa_check.py, build_docx.py, …)
  reference/          Content production reference files (loaded dynamically by pipeline)
  output/             Generated page files (per-slug subfolders)
  research/           SERP research data (per-keyword subfolders)
  logs/               Research subprocess logs
```
