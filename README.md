# Content Gen System

A platform-agnostic web app for running a multi-step AI content production pipeline.
Bring your own reference files, prompt templates, and API key — the system handles the rest.

---

## What it does

Takes a keyword → runs SERP research → generates a content brief → drafts a full page → humanizes and QA-checks the draft → delivers publish-ready and review output files.

The pipeline runs entirely in the browser UI. No VS Code or IDE required.

---

## Requirements

Before installing, make sure you have:

- **Python 3.9+** (`python3 --version`)
- **Google Chrome** installed (needed for SERP research only)
- An **Anthropic** or **OpenAI** API key

---

## Installation

**Step 1 — Clone the repo**

```bash
git clone https://github.com/arun-john-8846/content-gen-system.git
cd content-gen-system
```

**Step 2 — Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Step 3 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4 — Install Playwright browsers** (needed for SERP research only)

```bash
playwright install chromium
```

**Step 5 — Set your API key**

```bash
cp .env.example .env
```

Open `.env` and set your key:

```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

Or use OpenAI:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**Step 6 — Start the app**

```bash
python app.py
```

Open **http://localhost:5001** in your browser.

---

## First-time setup

Before creating content, complete these three setup steps in **Settings**.

### Step A — API key

Go to **Settings** (`/settings`). Confirm your LLM provider and API key are set correctly. Click **Save**.

### Step B — Upload your reference files

Go to **Settings → Reference files** (`/settings/reference`).

Upload the files that define your content rules. The pipeline loads every file in the `reference/` folder automatically at each step — no configuration needed beyond uploading.

Recommended files to create and upload:

| Filename | What to put in it |
|---|---|
| `writer_instructions.md` | Your writing workflow, page structure rules, word count targets, heading rules |
| `style_guide.md` | House style: naming conventions, banned phrases, formatting rules, voice |
| `humanizer_guide.md` | AI pattern removal rules + list of protected product terminology |
| `content_examples.md` | 1–3 full examples of good published pages for the pipeline to match |
| `product_docs.md` | Your product's feature documentation — used to verify capability claims |
| `serp_instructions.md` | How to interpret SERP data, what to prioritise, PAA extraction rules |
| `interlinking_list.md` | Internal link targets (URL + anchor text) |
| `qa_rules.md` | Optional — add `BANNED: phrase` lines to flag specific strings in QA |

> All files ship as empty placeholders. Replace them with your own content.

### Step C — Review prompt templates

Go to **Settings → Prompt templates** (`/settings/prompts`).

Six prompts control the pipeline steps: brief, draft, humanize, fix, publish, review. The defaults are generic and work out of the box. Edit them to match your product, style, or workflow. Changes are saved to the database and take effect on the next pipeline run.

---

## How to use

### 1. Create a page

1. Click **New page** on the dashboard
2. Enter the target keyword (e.g. `file server auditing`) — the URL slug is generated automatically
3. Click **Create**

### 2. Run SERP research

From the page detail view, open the **Research** tab and click **Start research**.

> **Before you start:** Close Chrome completely, then connect to the VPN for your target audience's locale. SERP results vary by region — match the locale to where your readers are.

The research tool:
- Opens Chrome with your real profile (to avoid bot detection)
- Scrapes the AI Overview, People Also Ask questions, and top 10 organic results
- Extracts competitor page structure (headings, sections present, word count)
- Writes a structured `research_summary.md` to `research/<slug>/`

The research step is optional — you can skip it and run the pipeline directly if you have a brief ready.

### 3. Run the pipeline

Open the **Pipeline** tab and click **Start pipeline**. Six steps run in sequence:

| # | Step | What happens |
|---|---|---|
| 1 | **Brief** | Generates a content brief from the research summary and all reference files |
| 2 | **Brief review** | Pauses for your approval — edit the brief in the UI if needed, then click **Approve** to continue |
| 3 | **Draft** | Writes the full page draft using the approved brief and reference files |
| 4 | **Humanize + QA** | Removes AI writing patterns, runs QA checks, auto-fixes em dashes and passive voice |
| 5 | **Publish** | Produces the clean publish-ready version with meta variants and internal links |
| 6 | **Review** | Produces the review document: QA scorecard, research notes, pipeline log |

Each step streams live output to the UI. You can cancel at any point.

### 4. Download output files

When the pipeline completes, open the **Files** tab:

- `<slug>_publish.docx` — clean, publish-ready page (meta variants + internal links only)
- `<slug>_review.docx` — QA scorecard, research notes, and full pipeline log

---

## Environment variables

All variables can also be set via the **Settings** page. Environment variables take priority over database settings.

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | — | Your Anthropic API key |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-5-20251022` | Anthropic model |
| `OPENAI_API_KEY` | — | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | OpenAI model |
| `USE_MCP_SERVER` | `false` | Route LLM calls via MCP server |
| `MCP_SERVER_URL` | — | MCP server URL (e.g. `http://localhost:8090`) |
| `FLASK_SECRET_KEY` | `content-gen-web-2026` | Flask session secret — change in production |
| `DATABASE_PATH` | `./adap.db` | SQLite file path |
| `PORT` | `5001` | Server port |

---

## SERP research — local only

`serp_research.py` uses a real persistent Chrome profile. It **cannot run on a cloud server** — it requires a local Chrome installation and a logged-in Google profile.

**Workflow when using a cloud deploy for the pipeline:**
1. Run research locally — results are written to `research/<slug>/`
2. Sync the `research/` folder to the cloud volume (rsync, Fly.io volume transfer, etc.)
3. Run the pipeline on the cloud app — it reads the research summaries and does not need Chrome

---

## Deployment

### Fly.io

```bash
brew install flyctl
flyctl auth login
flyctl launch --no-deploy
flyctl volumes create content_gen_data --size 5 --region lax
flyctl secrets set FLASK_SECRET_KEY="$(openssl rand -hex 32)"
flyctl secrets set ANTHROPIC_API_KEY="sk-ant-..."
flyctl secrets set LLM_PROVIDER="anthropic"
flyctl deploy
```

### Docker (local)

```bash
docker compose up --build
# Open http://localhost:5001
```

---

## MCP server (optional)

Exposes `llm_proxy` and `run_pipeline` tools for use with Claude Desktop, Cursor, or any MCP-compatible client.

**Stdio mode:**
```bash
python mcp_server.py
```

Claude Desktop config (`~/.claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "content-gen": {
      "command": "python",
      "args": ["/path/to/content-gen-system/mcp_server.py"],
      "env": { "ANTHROPIC_API_KEY": "sk-ant-...", "LLM_PROVIDER": "anthropic" }
    }
  }
}
```

**SSE/HTTP mode:**
```bash
python mcp_server.py --sse --port 8090
```
Then in Settings, enable MCP and set the server URL to `http://localhost:8090`.

---

## Project structure

```
content-gen-system/
  app.py                    Flask app — routes and views
  pipeline.py               LLM pipeline (brief → draft → humanize+QA → deliver)
  llm_client.py             Anthropic / OpenAI / MCP abstraction
  mcp_server.py             MCP server (stdio + SSE modes)
  config.py                 Settings loader (env → DB → defaults)
  models.py                 SQLite schema + CRUD
  jobs.py                   Research subprocess runner
  requirements.txt
  .env.example
  Dockerfile
  fly.toml
  docker-compose.yml
  static/
    app.js                  Pipeline SSE + research log polling
    style.css
  templates/
    base.html               Base layout and nav
    dashboard.html          Page list
    new_page.html           Create page form
    page_detail.html        Page tabs: Research, Pipeline, Files
    settings.html           API key and LLM provider
    settings_prompts.html   Edit per-step pipeline prompts
    settings_reference.html Upload and manage reference files
    research_view.html      Research log viewer
  tools/
    serp_research.py        SERP scraper (Playwright + Chrome)
    qa_check.py             QA checker (em dash, POV, AI patterns, custom rules)
    build_docx.py           Markdown → .docx converter
    flow_check.py           Page structure validator
    batch_structural_fix.py Batch auto-fix tool
    setup.sh                One-time setup helper script
  reference/                Content rules — upload your own files here
  output/                   Generated files (per-slug subfolders)
  research/                 SERP research data (per-keyword subfolders)
  logs/                     Research subprocess logs
```


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

## How to use

### 1. Configure settings

Before creating any pages, go to **Settings** (`/settings`) and fill in:

- **LLM provider** — choose Anthropic or OpenAI and paste your API key
- **Prompt templates** (`/settings/prompts`) — review and customise the six pipeline step prompts (brief, draft, humanize, fix, publish, review). The defaults work out of the box but can be tailored to your product or style
- **Reference files** (`/settings/reference`) — upload your content reference files (`.md`, `.docx`, or `.txt`). The pipeline loads all files in `reference/` automatically at each step. Recommended files to add:

| Filename | Purpose |
|---|---|
| `writer_instructions.md` | Full writing workflow and structural rules |
| `style_guide.md` | House style, terminology, and grammar rules |
| `content_examples.md` | Page template and canonical section examples |
| `humanizer_guide.md` | AI pattern removal rules |
| `serp_instructions.md` | SERP research and PAA extraction guide |
| `product_docs.md` | Product capability reference for accuracy checks |
| `interlinking_list.md` | Internal link candidates |
| `qa_rules.md` | Optional: custom `BANNED:` string rules for the QA checker |

### 2. Create a page

1. Click **New page** on the dashboard
2. Enter the target keyword (e.g. `file server auditing`) — the slug is auto-generated
3. Click **Create**

### 3. Run SERP research (optional but recommended)

From the page detail view, open the **Research** tab and click **Start research**.

This launches `serp_research.py` which:
- Scrapes the Google SERP (AI Overview, PAA, top 10 results)
- Extracts competitor headings and page structure
- Writes a structured research summary to `research/<slug>/`

> **Network requirement:** SERP research uses a real local Chrome profile. Connect to the network region that matches your target audience's Google locale before running research. For example, if you are writing for a US audience, connect via a US-based VPN.

### 4. Run the pipeline

Open the **Pipeline** tab and click **Start pipeline**. The pipeline runs six steps in sequence:

| Step | What happens |
|---|---|
| **Brief** | Generates a content brief from the research summary and reference files |
| **Brief review** | Pauses for your approval — edit the brief directly in the UI if needed, then click Approve |
| **Draft** | Writes the full page draft using the approved brief and all reference files |
| **Humanize + QA** | Removes AI writing patterns, runs the QA checker, auto-fixes em dashes and passive voice |
| **Publish** | Produces the clean publish-ready version |
| **Review** | Produces the review document (QA scorecard + research notes) |

Each step streams live output to the UI. You can cancel at any point.

### 5. Download output files

Once the pipeline completes, go to the **Files** tab to download:
- `<slug>_publish.docx` — clean publishable page with internal links only
- `<slug>_review.docx` — QA scorecard, research notes, and pipeline log

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
- A local Chrome installation with a persistent profile signed into Google
- A network connection matching the target locale for your SERP data (configure your VPN accordingly before running research)

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
