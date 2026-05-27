"""
Python pipeline — port of extension/src/chat/backgroundPipeline.ts

Runs the full brief → draft → humanize+QA → deliver sequence
without any VS Code dependency.

Usage:
    import pipeline
    pipeline.start_pipeline_thread(slug)   # fire and forget
    pipeline.get_log(slug)                  # returns list of log lines
    pipeline.cancel_pipeline(slug)          # sets cancellation flag
"""

import re
import subprocess
import sys
import threading
from collections import deque
from datetime import date
from pathlib import Path
from typing import Callable

import llm_client
import models

PROJECT_ROOT = Path(__file__).parent
MAX_FIX_ITERATIONS = 3

# Per-slug state: (thread, cancel_event, log_deque)
_PIPELINE_STATE: dict = {}
_STATE_LOCK = threading.Lock()


# ── File helpers ──────────────────────────────────────────────────────────────

def _read_ref(rel_path: str) -> str:
    full = PROJECT_ROOT / rel_path
    if not full.exists():
        return f"[File not found: {rel_path}]"
    return full.read_text(encoding="utf-8")


def _save_output(slug: str, filename: str, content: str) -> None:
    out_dir = PROJECT_ROOT / "output" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / filename).write_text(content, encoding="utf-8")


def _read_output(slug: str, filename: str) -> str:
    p = PROJECT_ROOT / "output" / slug / filename
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _output_exists(slug: str, filename: str) -> bool:
    return (PROJECT_ROOT / "output" / slug / filename).exists()


# ── Programmatic repair (deterministic last-resort fix) ───────────────────────

def _split_sentences(para: str) -> list[str]:
    result = []
    current = ""
    i = 0
    while i < len(para):
        ch = para[i]
        current += ch
        if ch in ".?!" and i + 2 < len(para) and para[i + 1] == " " and para[i + 2].isupper():
            current += " "
            i += 2
            result.append(current)
            current = ""
        else:
            i += 1
    if current.strip():
        result.append(current)
    return result


def _split_long_paragraphs(text: str) -> str:
    parts = []
    for para in text.split("\n\n"):
        trimmed = para.lstrip()
        skip = (
            trimmed.startswith("#")
            or trimmed.startswith("-")
            or trimmed.startswith("|")
            or trimmed.startswith("```")
            or trimmed.startswith("ADD SCREENSHOT")
            or trimmed.startswith("[")
            or re.match(r"^\d+\.", trimmed)
            or trimmed.startswith("Alt text")
        )
        if skip:
            parts.append(para)
            continue
        sentences = _split_sentences(para)
        if len(sentences) >= 4:
            first = "".join(sentences[:3]).rstrip()
            rest = "".join(sentences[3:]).lstrip()
            parts.append(f"{first}\n\n{rest}" if rest else first)
        else:
            parts.append(para)
    return "\n\n".join(parts)


def _programmatic_fix(text: str) -> str:
    """Deterministic em-dash removal + paragraph splitting."""
    fixed = text.replace("\u2014", ",")
    fixed = _split_long_paragraphs(fixed)
    return fixed


def _load_all_reference_files() -> str:
    """Load all .md files from the reference/ folder and return them concatenated."""
    ref_dir = PROJECT_ROOT / "reference"
    parts = []
    for md_file in sorted(ref_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        parts.append(f"## {md_file.name}\n\n{content}")
    if not parts:
        return "[No reference files found in reference/ folder. Add .md files to guide the pipeline.]"
    return "\n\n---\n\n".join(parts)


# ── QA helper ─────────────────────────────────────────────────────────────────

def _run_qa(slug: str) -> tuple[str, int]:
    """Run qa_check.py against the draft. Returns (output, total_issues)."""
    draft_path = PROJECT_ROOT / "output" / slug / f"{slug}_draft.md"
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "tools" / "qa_check.py"), str(draft_path)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    output = result.stdout + result.stderr
    m = re.search(r"TOTAL GENUINE ISSUES:\s*(\d+)", output)
    total = int(m.group(1)) if m else (-1 if not output.strip() else 0)
    return output, total


def _qa_failure_lines(output: str) -> str:
    """Extract only the violation lines from qa_check.py output."""
    lines = []
    for line in output.split("\n"):
        t = line.strip()
        if (
            t.startswith("[")
            or t.startswith("...")
            or t.startswith("Check:")
            or t.startswith("WARNING:")
            or t.startswith("FAIL:")
            or t.startswith("FOUND:")
            or re.match(r"^\s+\.\.\.", line)
        ):
            lines.append(line)
    return "\n".join(lines)


# ── Step 1: Brief ─────────────────────────────────────────────────────────────

def generate_brief(
    slug: str, page: dict, cluster_keywords: list, research_context: str,
    log: Callable[[str], None], cancel: threading.Event
) -> bool:
    brief_filename = f"{slug}_brief.md"
    if _output_exists(slug, brief_filename):
        log("Brief already exists — skipping generation.")
        models.add_step_event(slug, 2, "brief_approved")
        log("Brief ready (auto-approved).")
        return True

    log("Step 1/4 — Generating content brief...")

    ref_content = _load_all_reference_files()

    system = (
        "You are an expert content writer. "
        "Follow the writer instructions in the reference files exactly.\n\n"
        "## Reference files\n\n"
        + ref_content
    )

    user = (
        f"{research_context}\n\n---\n\n"
        f"Produce the full content brief for:\n"
        f"- **Slug:** {slug}\n"
        f"- **Seed keyword:** {page['seed_keyword']}\n"
        f"- **Cluster keywords:** {', '.join(cluster_keywords) or 'none'}\n\n"
        "Follow the writer instructions (Step 1) from the reference files exactly. "
        "Output ONLY the content brief markdown — no preamble, no explanation."
    )

    if cancel.is_set():
        log("Cancelled.")
        return False

    try:
        content = llm_client.send(system, user)
        _save_output(slug, brief_filename, content)
    except llm_client.LLMError as exc:
        log(f"Brief generation failed: {exc}")
        return False

    models.add_step_event(slug, 2, "brief_approved")
    log("Brief saved (auto-approved).")
    return True


# ── Step 2: Draft ─────────────────────────────────────────────────────────────

def generate_draft(
    slug: str, log: Callable[[str], None], cancel: threading.Event
) -> bool:
    log("Step 2/4 — Writing feature page draft...")

    brief_content = _read_output(slug, f"{slug}_brief.md")
    if not brief_content:
        log("Brief file not found. Cannot generate draft.")
        return False

    ref_content = _load_all_reference_files()

    system = (
        "You are an expert content writer. "
        "Follow the writer instructions in the reference files exactly.\n\n"
        "## Reference files\n\n"
        + ref_content
        + "\n\n---\n\n## HARD PROHIBITION \u2014 EM DASHES\n\n"
        "The em dash character (\u2014, Unicode U+2014) is BANNED from this output. "
        "Use a comma, semicolon, colon, or parentheses instead. Zero em dashes allowed."
    )

    user = (
        f"## Approved content brief\n\n{brief_content}\n\n---\n\n"
        f"Write the full feature page draft for slug **{slug}**.\n\n"
        "Follow the writer instructions (Step 2) from the reference files. "
        "Output ONLY the raw draft markdown — no preamble, no explanation."
    )

    if cancel.is_set():
        log("Cancelled.")
        return False

    try:
        content = llm_client.send(system, user)
        _save_output(slug, f"{slug}_draft.md", content)
        log("Draft saved.")
        return True
    except llm_client.LLMError as exc:
        log(f"Draft generation failed: {exc}")
        return False


# ── Step 3: Humanize + QA loop ────────────────────────────────────────────────

_HUMANIZE_SYSTEM = (
    "You are an AI pattern removal specialist. Apply the humanizer skill exactly.\n\n"
    "## Humanizer skill\n\n{humanizer}\n\n---\n\n## Style guide\n\n{style}\n\n---\n\n"
    "## HARD PROHIBITION — EM DASHES\n\n"
    "The em dash character (\u2014, Unicode U+2014) is BANNED from this output entirely.\n"
    "This applies whether spaced ( \u2014 ) or unspaced (\u2014). They are the same character.\n"
    "Do NOT introduce an em dash anywhere. If the input contains em dashes, replace every "
    "one with a comma, semicolon, colon, or parentheses.\n"
    "Zero em dashes must remain in the output."
)

_FIX_SYSTEM = (
    "You are a precise copy editor. Your only job is to fix the exact violations listed "
    "in the QA report. Do not rephrase, rewrite, or alter anything else.\n\n"
    "### Em dash rule (highest priority)\n"
    "Replace EVERY em dash character (U+2014) with context-appropriate punctuation:\n"
    "- List item separator  \u2192  colon\n"
    "- Parenthetical clause  \u2192  parentheses\n"
    "- Clause connector  \u2192  comma or semicolon\n"
    "- Screenshot placeholder  \u2192  colon\n"
    "Zero em dashes must remain.\n\n"
    "### Paragraph rule\n"
    "Paragraphs with 4+ sentences \u2192 split into two paragraphs of 2\u20133 sentences each.\n\n"
    "### Passive voice rule\n"
    "Rewrite \"was/were [past participle] by\" as active voice. Minimal surrounding changes.\n\n"
    "OUTPUT: Return ONLY the corrected full draft markdown. No preamble. No explanation."
)


def _do_humanize(slug: str, log: Callable[[str], None]) -> bool:
    """Single humanize pass. Returns True on success."""
    humanizer = _read_ref("reference/humanizer_guide.md")
    style = _read_ref("reference/style_guide.md")
    system = _HUMANIZE_SYSTEM.format(humanizer=humanizer, style=style)

    current = _read_output(slug, f"{slug}_draft.md")
    if not current:
        log("Draft file not found for humanization.")
        return False

    user = (
        "Apply the full humanization process from the humanizer skill to this draft.\n"
        "Protect all Type A, B, C, and D terms. Remove all AI writing patterns.\n"
        "CRITICAL: Do not use em dashes (\u2014) anywhere in the output. "
        "Replace any you encounter. Introduce zero new ones.\n"
        "Output ONLY the humanized draft markdown — no preamble, no explanation.\n\n"
        f"## Draft\n\n{current}"
    )

    try:
        log("  Humanizing draft...")
        result = llm_client.send(system, user)
        _save_output(slug, f"{slug}_draft.md", result)
        log("  Humanization done.")
        return True
    except llm_client.LLMError as exc:
        log(f"  Humanization failed ({exc}). Applying programmatic repair as fallback...")
        try:
            repaired = _programmatic_fix(current)
            _save_output(slug, f"{slug}_draft.md", repaired)
            log("  Programmatic repair applied as humanization fallback.")
            return True
        except Exception as repair_exc:
            log(f"  Programmatic repair also failed: {repair_exc}")
            return False


def humanize_and_qa_loop(
    slug: str, log: Callable[[str], None], cancel: threading.Event
) -> bool:
    log("Step 3/4 — Humanize + QA loop...")

    # Initial humanize pass
    if not _do_humanize(slug, log):
        return False

    for iteration in range(1, MAX_FIX_ITERATIONS + 1):
        if cancel.is_set():
            log("Cancelled.")
            return False

        log(f"  QA pass {iteration}/{MAX_FIX_ITERATIONS}...")
        qa_output, total = _run_qa(slug)

        if total == -1:
            log("QA script returned no output (possible crash). Check tools/qa_check.py.")
            return False

        if total == 0:
            models.add_step_event(slug, 5, "humanized")
            models.add_step_event(slug, 3, "qa_ran", {"output": qa_output, "total_issues": 0})
            log("QA clean — zero issues.")
            return True

        models.add_step_event(slug, 3, "qa_ran", {"output": qa_output, "total_issues": total})

        if iteration < MAX_FIX_ITERATIONS:
            log(f"  {total} issue(s) found. Running targeted fix + re-humanize...")
            failure_lines = _qa_failure_lines(qa_output)
            current = _read_output(slug, f"{slug}_draft.md")

            try:
                fixed = llm_client.send(
                    _FIX_SYSTEM,
                    f"## QA violations to fix\n\n```\n{failure_lines}\n```\n\n## Draft\n\n{current}",
                )
                _save_output(slug, f"{slug}_draft.md", fixed)
                log("  Targeted fix applied.")
            except llm_client.LLMError as exc:
                log(f"  Targeted fix failed: {exc}")
                return False

            if not _do_humanize(slug, log):
                return False
        else:
            log(
                f"  {total} issue(s) still remain after {MAX_FIX_ITERATIONS - 1} LLM fix attempts. "
                "Running programmatic repair..."
            )
            current = _read_output(slug, f"{slug}_draft.md")
            repaired = _programmatic_fix(current)
            _save_output(slug, f"{slug}_draft.md", repaired)
            log("  Programmatic repair applied (em dashes + paragraph splits).")

            log("  Final QA pass after programmatic repair...")
            final_output, final_total = _run_qa(slug)
            models.add_step_event(slug, 3, "qa_ran", {"output": final_output, "total_issues": final_total})
            if final_total == 0:
                models.add_step_event(slug, 5, "humanized")
                log("QA clean after programmatic repair — zero issues.")
                return True
            else:
                log(
                    f"  {final_total} issue(s) remain after programmatic repair. "
                    "Manual fix required — use the QA tab to run checks manually."
                )

    return True  # best-effort; delivery gated separately


# ── Step 4: Deliver ───────────────────────────────────────────────────────────

_PUBLISH_SYSTEM = """You are an expert SEO content writer producing the PUBLISH file for a feature page.

Output the file in EXACTLY this format:

## META BLOCK

Meta title A (N characters): [text]
Meta title B (N characters): [text]
Meta title C (N characters): [text]

Meta description A (N characters): [text]
Meta description B (N characters): [text]
Meta description C (N characters): [text]

---

## PAGE CONTENT

---

[full page content with internal links applied]

Meta title rules:
- Three distinct variants — not minor wording changes
- Each variant must include the primary keyword and the product name
- Title case throughout; maximum 60 characters per variant
- Do not repeat the same opening word across variants
- Count actual characters and include the count in parentheses

Meta description rules:
- 150–160 characters each (count actual characters and include the count)
- Sentence case; second person (you/your)
- Each must include a specific capability claim and a CTA or benefit signal
- No variant opens with the same phrase as another
- Lead with the benefit or the user's problem, not the product name

Internal linking rules:
- Apply 6–12 contextually earned internal links to the page content
- Anchor text must be a specific noun/phrase already present in the body prose
- No self-links; no competitor comparison or whitepaper page links
- Format as markdown hyperlinks: [anchor text](URL)
- Only add links if an interlinking list is provided below

Page content rules:
- Do NOT rewrite, add, or remove any body content — the draft is QA-clean
- Only change: insert internal links as markdown hyperlinks on existing anchor phrases
- Every link must be genuinely contextually relevant — do not force links

INTERLINKING LIST:
{interlinks}"""

_REVIEW_SYSTEM = """You are a QA specialist producing the REVIEW file for a content page — internal only, never published.

Output format:

# REVIEW DOC — [Page title derived from slug]
**Slug:** [slug]
**Date completed:** [today]
**Status:** Pipeline complete. External gates (grammar check, plagiarism check, AI humanizer check) pending.

---

## Part A — Compliance scorecard

| Category | Score | Max | Status | Notes |
|---|---|---|---|---|
| Style guide | [score] | 75 | [GREEN/YELLOW/RED] | [detailed notes] |
| Humanization | [score] | 50 | [GREEN/YELLOW/RED] | [detailed notes] |
| Product accuracy | [score] | 50 | [GREEN/YELLOW/RED] | [detailed notes] |
| SERP and content strategy | [score] | 65 | [GREEN/YELLOW/RED] | [detailed notes] |
| **TOTAL** | **[total]** | **240** | **[PASS/MINOR ISSUES/NEEDS WORK]** | **[%] — [status]** |

Status key: GREEN = full marks or ≤2 pt deviation. YELLOW = minor deviation noted. RED = fix required.
PASS = ≥225/240 (≥93.75%). MINOR ISSUES = 200–224. NEEDS WORK = <200.

Scoring criteria summary:

Style guide (75 pts): second person throughout (-3 each violation), active voice (-2 each passive), paragraphs ≤3 sentences (-2 each), no rhetorical openers (-2), no framing sentences (-2), no short-sentence stacking (-2), sentence case headings (-2 each), Oxford comma (-1 each missing), zero em dashes (-5 if any), correct naming conventions per style_guide.md, three meta title variants 50–60 chars (-5 if absent), three meta description variants 150–160 chars (-5 if absent).

Humanization (50 pts): no dangling -ing clause openers (-3 each), no generic closers (-2 each), no wordy phrases (-2 each), no AI vocabulary words like leverage/utilize/seamlessly/robust/streamline/enhance (-3 each), domain expert posture throughout (-2 each hedging statement), no bureaucratic setup lines (-2 each), no closing bullets that restate preceding content (-2 each).

Product accuracy (50 pts): all capability claims verifiable in product_docs.md (-5 per unverified claim), no out-of-scope features claimed (-10 per violation), compliance standard names correctly formatted (-2 per error).

SERP and content strategy (65 pts): table-stakes topics covered, FAQ with 5–6 live PAA questions (-5 if absent or wrong count), screenshot placeholders correctly formatted (-3 each missing), word count within target range (-5 if significantly outside), internal links applied 6–12 (-5 if absent), links recorded in review doc.

After the scorecard:

---

## Part B — Internal links applied

List each internal link in the publish file:
| Anchor text | Destination URL | Section |
|---|---|---|

---

## Part C — QA and production notes

- Em dash removal: [final count zero / any remaining]
- QA pass: [issues found and how resolved]
- Humanization: [AI patterns identified and removed]
- External gates pending: grammar check, plagiarism check, AI humanizer detection check"""


def deliver(
    slug: str, log: Callable[[str], None], cancel: threading.Event
) -> bool:
    """Gate-checked delivery: runs a final QA then generates publish + review files + .docx."""
    log("Step 4/4 — Pre-delivery QA gate...")

    qa_output, total = _run_qa(slug)
    if total > 0:
        log(
            f"Delivery blocked — {total} QA issue(s) still present. "
            "Fix manually before delivering."
        )
        return False

    log("QA gate passed. Generating delivery files...")

    final_draft = _read_output(slug, f"{slug}_draft.md")
    # Load interlinking list if present (users add reference/interlinking_list.md)
    interlinks_path = PROJECT_ROOT / "reference" / "interlinking_list.md"
    interlinks = interlinks_path.read_text(encoding="utf-8") if interlinks_path.exists() else "(No interlinking list found. Add reference/interlinking_list.md to enable internal links.)"
    today = date.today().strftime("%B %-d, %Y")

    # ── Publish file ─────────────────────────────────────────────────────────
    if not _output_exists(slug, f"{slug}_publish.md"):
        if cancel.is_set():
            log("Cancelled.")
            return False
        try:
            log("  Generating publish file...")
            publish_content = llm_client.send(
                _PUBLISH_SYSTEM.format(interlinks=interlinks),
                f"Slug: {slug}\n\nDraft content:\n\n{final_draft}\n\n"
                "Generate the complete publish file following the format exactly.",
            )
            _save_output(slug, f"{slug}_publish.md", publish_content)
            log("  Publish file saved.")
        except llm_client.LLMError as exc:
            log(f"  Publish file failed: {exc}")
            return False
    else:
        log("  Publish file already exists — skipping.")

    # ── Review file ───────────────────────────────────────────────────────────
    if not _output_exists(slug, f"{slug}_review.md"):
        if cancel.is_set():
            log("Cancelled.")
            return False
        try:
            log("  Generating review file...")
            review_content = llm_client.send(
                _REVIEW_SYSTEM,
                f"Slug: {slug}\nDate: {today}\n\nDraft content:\n\n{final_draft}\n\n"
                "Score honestly. If the draft is clean in a category, give full marks and "
                "say so. If there are issues, identify them specifically with deductions.",
            )
            _save_output(slug, f"{slug}_review.md", review_content)
            log("  Review file saved.")
        except llm_client.LLMError as exc:
            log(f"  Review file failed: {exc}")
            return False
    else:
        log("  Review file already exists — skipping.")

    # ── Build .docx ───────────────────────────────────────────────────────────
    log("  Building .docx files...")
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "tools" / "build_docx.py"), slug],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    if result.returncode == 0:
        models.add_step_event(slug, 6, "docx_built")
        log(f'Pipeline complete for "{slug}". Open the Delivery tab to access your files.')
        return True
    else:
        log(f"  .docx build failed: {result.stdout}\n{result.stderr}")
        log("  Markdown files are saved — use Build .docx in the Delivery tab to retry.")
        return False


# ── Full auto pipeline ────────────────────────────────────────────────────────

def run_auto_pipeline(
    slug: str, log: Callable[[str], None], cancel: threading.Event
) -> bool:
    """
    Full pipeline: brief → draft → humanize+QA → deliver.
    Returns True on full success, False on any failure.
    """
    page = models.get_page(slug)
    if not page:
        log(f'Page "{slug}" not found in database.')
        return False

    cluster_keywords = models.get_cluster_keywords(page)
    all_keywords = [page["seed_keyword"]] + cluster_keywords

    # Collect research summaries
    research_parts = []
    for kw in all_keywords:
        kw_slug = re.sub(r"[^a-z0-9]+", "-", kw.lower()).strip("-")
        summary_path = PROJECT_ROOT / "research" / kw_slug / "research_summary.md"
        if summary_path.exists():
            research_parts.append(
                f"### Research summary: {kw}\n\n{summary_path.read_text(encoding='utf-8')}"
            )

    if not research_parts:
        log("No research summaries found. Run research first.")
        return False

    research_context = "## Research summaries\n\n" + "\n\n---\n\n".join(research_parts)

    log(f'Starting auto pipeline for "{slug}"...')

    if not generate_brief(slug, page, cluster_keywords, research_context, log, cancel):
        return False
    if cancel.is_set():
        log("Cancelled.")
        return False

    if not generate_draft(slug, log, cancel):
        return False
    if cancel.is_set():
        log("Cancelled.")
        return False

    if not humanize_and_qa_loop(slug, log, cancel):
        return False
    if cancel.is_set():
        log("Cancelled.")
        return False

    return deliver(slug, log, cancel)


# ── Background thread management ──────────────────────────────────────────────

def start_pipeline_thread(slug: str) -> bool:
    """
    Start the auto pipeline in a background thread.
    Returns False if a pipeline is already running for this slug.
    """
    with _STATE_LOCK:
        existing = _PIPELINE_STATE.get(slug)
        if existing and existing[0].is_alive():
            return False  # already running

        log_deque: deque = deque(maxlen=500)
        cancel_event = threading.Event()

        def _log(msg: str) -> None:
            log_deque.append(msg)

        def _run() -> None:
            try:
                run_auto_pipeline(slug, _log, cancel_event)
            except Exception as exc:
                _log(f"Pipeline error: {exc}")

        t = threading.Thread(target=_run, daemon=True, name=f"pipeline-{slug}")
        _PIPELINE_STATE[slug] = (t, cancel_event, log_deque)
        t.start()
        return True


def get_log(slug: str) -> list:
    """Return all accumulated log lines for a slug."""
    state = _PIPELINE_STATE.get(slug)
    if not state:
        return []
    return list(state[2])


def get_log_from(slug: str, offset: int) -> tuple:
    """Return new log lines since offset and the new offset."""
    lines = get_log(slug)
    new_lines = lines[offset:]
    return new_lines, len(lines)


def is_running(slug: str) -> bool:
    """Return True if a pipeline thread is currently active for this slug."""
    state = _PIPELINE_STATE.get(slug)
    return bool(state and state[0].is_alive())


def cancel_pipeline(slug: str) -> None:
    """Signal the pipeline thread for this slug to stop at the next checkpoint."""
    state = _PIPELINE_STATE.get(slug)
    if state:
        state[1].set()
