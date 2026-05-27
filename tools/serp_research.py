#!/usr/bin/env python3
"""
SERP Research Tool — Content Gen Pipeline
==========================================
Uses your real Chrome profile to avoid bot detection (Option C).

Requirements:
  - Chrome must be FULLY CLOSED before running
  - US VPN must be ACTIVE before running

Usage (single keyword):
  python tools/serp_research.py "active directory auditing"

Usage (seed + cluster keywords — sequential):
  python tools/serp_research.py "AD user activity monitoring" "user logon auditing" "privileged account monitoring"

  First keyword = seed keyword (researched first)
  Remaining keywords = cluster keywords (researched in order)

Usage (parallel — recommended for 2+ keywords):
  python tools/serp_research.py --parallel 3 "AD user activity monitoring" "user logon auditing" "privileged account monitoring"

  --parallel N  Run up to N keywords simultaneously, each in its own isolated
                Chromium instance and browser profile. Default batch size: 3.
                All keywords (seed + clusters) start in the first batch.

Output (one folder per keyword):
  research/<keyword-slug>/
    serp_data.json          — organic URLs, PAA questions, AI Overview
    competitor_01_<domain>.txt  — full text per competitor page
    competitor_02_<domain>.txt
    ...
    research_summary.md     — formatted summary ready for draft workflow
    rca_events.json         — structured event log for root cause analysis (errors, warnings, tracebacks)
"""

import sys
import json
import re
import time
import os
import shutil
import threading
import traceback
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus, urlparse

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("ERROR: Playwright not installed.")
    print("Run: pip install playwright && playwright install chrome")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────

GOOGLE_SEARCH_URL = "https://www.google.com/search"
RESULTS_DIR = Path(__file__).parent.parent / "research"
MAX_COMPETITORS = 10
PAGE_LOAD_TIMEOUT = 30_000   # ms
INTER_PAGE_DELAY = 3          # seconds between page fetches
MAX_PAGE_TEXT = 15_000        # chars per competitor page (keeps files manageable)

# Mutex so only one thread prompts for CAPTCHA at a time
_CAPTCHA_LOCK = threading.Lock()

# Per-thread RCA context: slug, accumulated events list, run start time
_thread_context = threading.local()


def _log(level: str, msg: str, step: str = "", exc_info: bool = False) -> None:
    """
    Emit a structured log line: [HH:MM:SS] [LEVEL] [slug] msg
    Also appends a structured event to _thread_context.events for rca_events.json.
    If exc_info=True, the current exception traceback is included in both.
    """
    slug = getattr(_thread_context, "slug", "main")
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] [{slug}] {msg}", flush=True)

    tb_text = ""
    if exc_info:
        raw = traceback.format_exc()
        if raw and raw.strip() not in ("", "NoneType: None"):
            tb_text = raw
            print(raw, flush=True)

    events: list = getattr(_thread_context, "events", None)
    if events is not None:
        event: dict = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "level": level,
            "step": step,
            "msg": msg,
        }
        if tb_text:
            event["traceback"] = tb_text
        events.append(event)


# ── Utilities ─────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def domain_from_url(url: str) -> str:
    return urlparse(url).netloc.replace("www.", "")

def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def save_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8")

def print_section(title: str):
    slug = getattr(_thread_context, "slug", "")
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = f"[{ts}] [{slug}] " if slug else f"[{ts}] "
    print(f"\n[{ts}] {'─'*56}")
    print(f"  {prefix}{title}")
    print(f"[{ts}] {'─'*56}")

def reset_browser_profile(profile_path: str):
    """
    Delete and recreate the Playwright browser profile directory.

    Always wiping the profile before each keyword run prevents two failure modes:
    1. Profile lock — a previous live Chromium session holds a lock file; a new
       launch detects "Opening in existing browser session", Playwright loses
       control, and the context closes immediately (about:blank stays open).
    2. Session state accumulation — repeated runs on the same profile build up
       cookies/history that trigger Google bot-detection mid-session, causing a
       redirect that closes the active page context between steps.
    """
    profile = Path(profile_path)
    if profile.exists():
        try:
            shutil.rmtree(profile)
            _log("INFO", f"Browser profile wiped: {profile_path}", step="reset_browser_profile")
        except Exception as e:
            _log("WARN", f"Could not wipe profile: {e}", step="reset_browser_profile", exc_info=True)
    profile.mkdir(parents=True, exist_ok=True)
    _log("INFO", f"Browser profile ready: {profile_path}", step="reset_browser_profile")

# ── SERP extraction ───────────────────────────────────────────────────────────

def extract_organic_urls(page) -> list:
    """
    Extract top 10 organic (non-ad) result URLs.
    Deduplicates by domain so each site appears once.
    """
    urls = []
    seen_domains = set()

    try:
        # Try multiple known Google result selectors — Google changes the DOM frequently
        selector_candidates = [
            "#rso .g a[href]",           # classic
            "#rso a[jsname][href]",       # newer variant
            "div[data-sokoban-container] a[href]",  # 2024+ layout
            "#search .g a[href]",
            "h3 > a[href]",              # broadest fallback: any linked h3
        ]
        result_links = []
        for sel in selector_candidates:
            result_links = page.query_selector_all(sel)
            if result_links:
                break

        for el in result_links:
            href = el.get_attribute("href") or ""
            if not href.startswith("http"):
                continue
            if "google.com" in href:
                continue
            # Skip Google-owned redirects like /url?q=...
            if href.startswith("https://www.google.com/url"):
                continue

            dom = domain_from_url(href)
            if dom in seen_domains:
                continue

            seen_domains.add(dom)
            urls.append(href)

            if len(urls) >= MAX_COMPETITORS:
                break

    except Exception as e:
        _log("WARN", f"Organic URL extraction error: {e}", step="extract_organic_urls", exc_info=True)

    return urls


def extract_paa_questions(page) -> list:
    """
    Extract People Also Ask questions using the data-q attribute.
    Expands the PAA box by clicking to load more questions first.
    """
    questions = []

    try:
        # Expand PAA box by clicking questions to reveal more
        for _ in range(4):
            paa_buttons = page.query_selector_all("[data-q]")
            if not paa_buttons:
                break
            # Click the last few visible questions to expand more
            for btn in paa_buttons[-3:]:
                try:
                    btn.click()
                    time.sleep(0.4)
                except Exception as _btn_err:
                    _log("WARN", f"PAA button click failed: {_btn_err}", step="extract_paa_expand", exc_info=True)

        # Now collect all data-q values
        elements = page.query_selector_all("[data-q]")
        for el in elements:
            q = (el.get_attribute("data-q") or "").strip()
            if q and q not in questions:
                questions.append(q)

    except Exception as e:
        _log("WARN", f"PAA extraction error: {e}", step="extract_paa_questions", exc_info=True)

    return questions


def extract_ai_overview(page) -> dict:
    """
    Detect and extract AI Overview content if present.
    Google changes AI Overview selectors frequently — tries multiple known patterns.
    """
    result = {"present": False, "text": "", "sources": []}

    # Known AI Overview container selectors (ordered by specificity)
    text_selectors = [
        "div[data-attrid='wa:/description']",
        "div[jscontroller='cF7kyd']",
        "search-generated-related-content",
        "div.Fm6ytb",
        "div.LGOjhe",
        "#ai-overview",
        "div[data-q]",
    ]

    try:
        for selector in text_selectors:
            el = page.query_selector(selector)
            if el:
                text = (el.inner_text() or "").strip()
                if len(text) > 150:
                    result["present"] = True
                    result["text"] = text[:3_000]
                    break

        # Collect source citations
        source_selectors = [
            "search-generated-related-content a[href]",
            "div.Fm6ytb a[href]",
            "#ai-overview a[href]",
        ]
        for sel in source_selectors:
            links = page.query_selector_all(sel)
            for link in links[:5]:
                href = link.get_attribute("href") or ""
                if href.startswith("http") and href not in result["sources"]:
                    result["sources"].append(href)
            if result["sources"]:
                break

    except Exception as e:
        _log("WARN", f"AI Overview extraction error: {e}", step="extract_ai_overview", exc_info=True)

    return result


# ── Competitor page fetcher ───────────────────────────────────────────────────

def fetch_competitor_page(page, url: str) -> dict:
    """
    Navigate to a competitor URL and extract:
    - Page title
    - All H1/H2/H3 headings (structure map)
    - Full body text (capped at MAX_PAGE_TEXT chars)
    - Word count
    """
    result = {
        "url": url,
        "domain": domain_from_url(url),
        "status": "unknown",
        "title": "",
        "word_count": 0,
        "headings": [],
        "full_text": "",
        "sections_present": [],
        "error": "",
    }

    try:
        response = page.goto(url, timeout=PAGE_LOAD_TIMEOUT, wait_until="domcontentloaded")

        if response and response.status >= 400:
            result["status"] = f"HTTP {response.status}"
            result["error"] = f"HTTP error {response.status}"
            return result

        # Give JS time to render
        time.sleep(2)

        # Check for redirect to homepage (common with guessed URLs)
        final_url = page.url
        if final_url.rstrip("/") in ["https://www.google.com", url.rstrip("/")]:
            pass  # fine
        elif domain_from_url(final_url) != domain_from_url(url):
            result["status"] = "redirected"
            result["error"] = f"Redirected to different domain: {final_url}"
            return result

        result["title"] = page.title()

        # Extract headings for structure map
        for tag in ["h1", "h2", "h3"]:
            els = page.query_selector_all(tag)
            for el in els:
                text = (el.inner_text() or "").strip()
                if text:
                    result["headings"].append({"tag": tag, "text": text})

        # Extract body text — try progressively broader containers
        full_text = ""
        for selector in ["main", "article", "[role='main']", "#content", ".content", "body"]:
            el = page.query_selector(selector)
            if el:
                text = el.inner_text() or ""
                if len(text) > 500:
                    full_text = text
                    break

        if not full_text:
            full_text = page.inner_text("body")

        result["full_text"] = full_text[:MAX_PAGE_TEXT]
        result["word_count"] = len(full_text.split())
        result["status"] = "success"

        # Detect which standard sections are present (for gap analysis)
        lower_text = full_text.lower()
        section_checks = {
            "definition": ["what is active directory", "what is ad audit", "what is ad"],
            "what_to_audit": ["what to audit", "key areas", "what should you audit"],
            "benefits": ["benefit", "why audit", "why is active directory auditing"],
            "privileged_users": ["privileged user", "domain admin", "admin account"],
            "logon_monitoring": ["logon monitor", "login monitor", "logon activity"],
            "gpo_auditing": ["group policy", "gpo"],
            "permissions": ["permission change", "acl change", "access control"],
            "alerting": ["real-time alert", "real time alert", "instant alert"],
            "uba": ["user behavior", "ueba", "anomaly detect", "machine learning"],
            "compliance": ["compliance", "hipaa", "sox", "pci", "gdpr"],
            "hybrid_cloud": ["azure", "entra", "hybrid", "cloud"],
            "native_tools": ["event viewer", "native tool", "powershell limitation", "built-in tool"],
            "faq": ["faq", "frequently asked"],
        }
        for section, keywords in section_checks.items():
            if any(kw in lower_text for kw in keywords):
                result["sections_present"].append(section)

    except PlaywrightTimeout:
        result["status"] = "timeout"
        result["error"] = "Page load timed out after 30s"
        _log("WARN", f"Timeout fetching competitor page: {url}", step="fetch_competitor_page")
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        _log("ERROR", f"Competitor page fetch failed: {url} — {e}", step="fetch_competitor_page", exc_info=True)

    return result


# ── Research summary generator ────────────────────────────────────────────────

def generate_summary(keyword: str, serp_data: dict, competitor_data: list) -> str:
    """
    Generate a formatted research_summary.md following the
    FP_PAA_and_SERP_instructions.md output format.
    """
    lines = []
    now = datetime.now().strftime("%B %d, %Y")

    lines += [
        f"# SERP Research Summary",
        f"",
        f"**Keyword:** {keyword}",
        f"**Date:** {now}",
        f"**Search parameters:** gl=us&hl=en&pws=0",
        f"**Tool:** Playwright + real Chrome profile (Option C)",
        f"",
        f"---",
        f"",
    ]

    # ── AI Overview ────────────────────────────────────────────────────────────
    lines.append("## AI Overview")
    ai = serp_data.get("ai_overview", {})
    if ai.get("present"):
        lines.append("**Present:** Yes")
        lines.append("")
        lines.append("**Opening answer / description:**")
        lines.append(f"> {ai['text'][:600].replace(chr(10), ' ')}")
        lines.append("")
        if ai.get("sources"):
            lines.append("**Source citations:**")
            for src in ai["sources"]:
                lines.append(f"- {src}")
        lines.append("")
        lines.append("**Gaps in AI Overview (what it missed):**")
        lines.append("_Review the text above and note missing topics here_")
    else:
        lines.append("**Present:** No — AI Overview did not appear for this keyword.")
    lines.append("")

    # ── Organic URLs ───────────────────────────────────────────────────────────
    lines.append("## Organic result URLs (top 10)")
    lines.append("")
    organic = serp_data.get("organic_urls", [])
    if organic:
        for i, url in enumerate(organic, 1):
            lines.append(f"{i}. {url}")
    else:
        lines.append("_No organic URLs extracted — check SERP extraction logs_")
    lines.append("")

    # ── PAA ────────────────────────────────────────────────────────────────────
    lines.append("## PAA questions (People Also Ask)")
    lines.append("")
    paa = serp_data.get("paa_questions", [])
    if paa:
        for q in paa:
            lines.append(f"- {q}")
    else:
        lines.append("No PAA box appeared for this keyword (normal for high-intent product keywords).")
    lines.append("")

    # ── Own page (client's own domain result) ────────────────────────────────
    lines.append("## Client's own page")
    lines.append("")
    me_result = next(
        (c for c in competitor_data if "manageengine.com" in c["domain"]), None
    )
    if me_result:
        pos = next(
            (i + 1 for i, u in enumerate(organic) if "manageengine.com" in u), "N/A"
        )
        lines.append(f"**Ranks:** Yes — position {pos}")
        lines.append(f"**URL:** {me_result['url']}")
        lines.append(f"**Word count:** ~{me_result['word_count']}")
        lines.append("")
        lines.append("**Sections and headings:**")
        for h in me_result["headings"]:
            lines.append(f"  {h['tag'].upper()}: {h['text']}")
        lines.append("")
        lines.append("**ME-owned sections competitors miss:**")
        lines.append("_Review competitor headings below and identify gaps_")
    else:
        lines.append("ME did not rank in top 10 for this keyword.")
    lines.append("")

    # ── Competitor analysis ────────────────────────────────────────────────────
    lines.append("## Competitor pages")
    lines.append("")
    competitors = [c for c in competitor_data if "manageengine.com" not in c["domain"]]

    for i, c in enumerate(competitors, 1):
        lines.append(f"### {i}. {c['domain']}")
        lines.append(f"**URL:** {c['url']}")
        lines.append(f"**Status:** {c['status']}")
        lines.append(f"**Word count:** ~{c['word_count']}")
        lines.append(f"**Sections present:** {', '.join(c['sections_present']) if c['sections_present'] else 'none detected'}")
        if c["headings"]:
            lines.append("**H2/H3 structure:**")
            for h in c["headings"]:
                if h["tag"] in ("h2", "h3"):
                    indent = "  " if h["tag"] == "h3" else ""
                    lines.append(f"  {indent}{h['tag'].upper()}: {h['text']}")
        if c["error"]:
            lines.append(f"**Error:** {c['error']}")
        lines.append("")

    # ── Gap analysis framework ─────────────────────────────────────────────────
    lines.append("## Content gap analysis")
    lines.append("")

    # Auto-detect table-stakes (sections found in 3+ competitors)
    section_counts = Counter()
    for c in competitors:
        for s in c.get("sections_present", []):
            section_counts[s] += 1

    table_stakes = [s for s, count in section_counts.items() if count >= 3]
    lines.append("**Table-stakes topics (3+ competitors cover these — must include):**")
    if table_stakes:
        for s in table_stakes:
            lines.append(f"- {s.replace('_', ' ').title()} ({section_counts[s]}/{len(competitors)} competitors)")
    else:
        lines.append("_Run review of competitor full_text to identify table-stakes_")
    lines.append("")

    lines.append("**ME-ownable gaps (competitors consistently miss):**")
    lines += [
        "- Account Lockout Analyzer with root cause identification",
        "- Attack Surface Analyzer — 25+ named AD attacks (Kerberoasting, Golden Ticket, DCSync, etc.)",
        "- Hybrid logon correlation (on-premises AD + Entra ID in single console)",
        "- Custom report profiles (save user + action + filter combinations)",
        "- Response automation (alert → auto-ticket → team notified)",
        "- AdminSDHolder Permission Changes as named, distinct audit area",
        "- Inactive/stale account monitoring as a distinct audit area",
    ]
    lines.append("")

    lines.append("---")
    lines.append(f"_Generated by tools/serp_research.py on {now}_")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def run_research_for_keyword(keyword: str, is_seed: bool = True):
    """Run the full SERP research pipeline for a single keyword."""
    slug = slugify(keyword)
    profile_path = str(Path(os.path.expanduser("~")) / f".playwright-research-profile-{slug}")
    output_dir = RESULTS_DIR / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialise per-thread RCA context
    _thread_context.slug = slug
    _thread_context.events = []
    _thread_context.started_at = datetime.now().isoformat(timespec="seconds")

    label = "SEED" if is_seed else "CLUSTER"

    print(f"\n{'='*60}")
    print(f"  SERP Research Tool — Content Gen Pipeline")
    print(f"{'='*60}")
    print(f"  Keyword   : {keyword} [{label}]")
    print(f"  Output    : {output_dir}")
    print(f"  Profile   : {profile_path}")
    print()
    print("  ⚠  US VPN must be ACTIVE.")
    print()
    reset_browser_profile(profile_path)
    print()

    print("  Launching browser...")

    serp_data = {
        "keyword": keyword,
        "date": datetime.now().isoformat(),
        "organic_urls": [],
        "paa_questions": [],
        "ai_overview": {"present": False, "text": "", "sources": []},
    }
    competitor_data = []

    with sync_playwright() as p:

        # ── Launch Playwright Chromium ─────────────────────────────────────
        print_section("Step 1 of 3 — Launching Browser")

        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=profile_path,
                headless=False,
                args=[
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--window-size=1280,900",
                ],
                ignore_default_args=["--enable-automation"],
                viewport={"width": 1280, "height": 900},
            )
        except Exception as e:
            _log("ERROR", f"Could not launch browser: {e}", step="browser_launch", exc_info=True)
            raise RuntimeError(f"Could not launch browser: {e}") from e

        page = browser.new_page()

        # ── Google SERP ───────────────────────────────────────────────────────
        print_section("Step 2 of 3 — Google SERP")
        search_url = (
            f"{GOOGLE_SEARCH_URL}"
            f"?q={quote_plus(keyword)}"
            f"&gl=us&hl=en&pws=0&num=10"
        )
        print(f"  URL: {search_url}")

        try:
            page.goto(search_url, timeout=PAGE_LOAD_TIMEOUT)
            time.sleep(4)  # let full JS render

            # ── CAPTCHA check ──────────────────────────────────────────────
            current_url = page.url
            if "sorry/index" in current_url or "captcha" in current_url.lower():
                _log("WARN", "CAPTCHA detected — awaiting manual solve", step="serp_load")
                with _CAPTCHA_LOCK:
                    stdin = sys.__stdin__ or sys.stdin
                    sys.__stdout__.write(f"\n  ⚠  [{slug}] CAPTCHA detected. Solve it in the Chrome window.\n")
                    sys.__stdout__.write("  Press Enter after solving the CAPTCHA... ")
                    sys.__stdout__.flush()
                    stdin.readline()
                time.sleep(2)

            # ── Confirm US results ─────────────────────────────────────────
            if "gl=us" in page.url:
                print("  ✓ US results confirmed")
            else:
                _log("WARN", "Could not confirm US results — VPN may not be active", step="serp_load")

            # ── Extract organic URLs ───────────────────────────────────────
            print("  Extracting organic URLs...")
            serp_data["organic_urls"] = extract_organic_urls(page)
            count = len(serp_data["organic_urls"])
            print(f"  Found {count} organic result(s)")
            for i, url in enumerate(serp_data["organic_urls"], 1):
                print(f"    {i:2}. {url}")

            if count == 0:
                _log("WARN", "No organic URLs found — possible CAPTCHA or VPN issue", step="extract_organic_urls")
                screenshot_path = str(output_dir / "serp_screenshot.png")
                try:
                    page.screenshot(path=screenshot_path, full_page=False)
                    _log("INFO", f"SERP screenshot saved → {screenshot_path}", step="extract_organic_urls")
                except Exception as _ss_err:
                    _log("WARN", f"Could not save SERP screenshot: {_ss_err}", step="extract_organic_urls", exc_info=True)

            # ── Page context health check ──────────────────────────────────
            # After URL extraction the page must still be on a Google SERP.
            # A bot-detection redirect (to about:blank, sorry/index, etc.) will
            # have navigated away and closed the renderer context.  Detect this
            # now so we abort with a clear message instead of letting all
            # competitor fetches silently fail with "Target page ... has been closed".
            try:
                current_url = page.url
                if "google.com/search" not in current_url:
                    _log("ERROR", f"Page context lost — current URL: {current_url} (bot detection redirect?)", step="page_context_check")
                    save_json(output_dir / "serp_data.json", serp_data)
                    _write_rca(output_dir, keyword, slug, outcome="failed")
                    browser.close()
                    return
            except Exception as health_err:
                _log("ERROR", f"Page context inaccessible: {health_err}", step="page_context_check", exc_info=True)
                save_json(output_dir / "serp_data.json", serp_data)
                _write_rca(output_dir, keyword, slug, outcome="failed")
                try:
                    browser.close()
                except Exception:
                    pass
                return

            # ── Extract PAA ────────────────────────────────────────────────
            print("  Extracting PAA questions...")
            serp_data["paa_questions"] = extract_paa_questions(page)
            paa_count = len(serp_data["paa_questions"])
            if paa_count:
                print(f"  Found {paa_count} PAA question(s):")
                for q in serp_data["paa_questions"]:
                    print(f"    - {q}")
            else:
                print("  No PAA box found (normal for product-intent keywords)")

            # ── Extract AI Overview ────────────────────────────────────────
            print("  Checking for AI Overview...")
            serp_data["ai_overview"] = extract_ai_overview(page)
            if serp_data["ai_overview"]["present"]:
                print("  ✓ AI Overview present")
            else:
                print("  No AI Overview for this keyword")

        except Exception as e:
            _log("ERROR", f"SERP step failed: {e}", step="serp_step", exc_info=True)

        save_json(output_dir / "serp_data.json", serp_data)
        print(f"\n  Saved → serp_data.json")

        # ── Fetch competitor pages ─────────────────────────────────────────
        print_section("Step 3 of 3 — Fetching competitor pages")

        total = len(serp_data["organic_urls"])
        for i, url in enumerate(serp_data["organic_urls"], 1):
            dom = domain_from_url(url)
            print(f"\n  [{i}/{total}] {dom}")
            print(f"  URL: {url}")

            result = fetch_competitor_page(page, url)
            competitor_data.append(result)

            # Save individual file
            safe_name = re.sub(r"[^a-z0-9]", "_", dom)
            outfile = output_dir / f"competitor_{i:02d}_{safe_name}.txt"
            content = (
                f"URL: {url}\n"
                f"Domain: {dom}\n"
                f"Status: {result['status']}\n"
                f"Word count: {result['word_count']}\n"
                f"Sections detected: {', '.join(result['sections_present'])}\n"
                f"\nHEADINGS:\n"
            )
            for h in result["headings"]:
                indent = "  " if h["tag"] == "h3" else ""
                content += f"  {indent}{h['tag'].upper()}: {h['text']}\n"
            content += f"\nFULL TEXT:\n{result['full_text']}"
            save_text(outfile, content)

            status_icon = "✓" if result["status"] == "success" else "✗"
            print(f"  {status_icon} {result['status']} | {result['word_count']} words | {outfile.name}")

            if result["error"]:
                level = "WARN" if result["status"] == "timeout" else "ERROR"
                _log(level, f"Competitor [{dom}]: {result['error']}", step="fetch_competitor_pages")

            time.sleep(INTER_PAGE_DELAY)

        save_json(output_dir / "competitor_data.json", competitor_data)
        browser.close()

    # ── Generate summary ───────────────────────────────────────────────────────
    print_section("Generating research summary")
    summary = generate_summary(keyword, serp_data, competitor_data)
    summary_file = output_dir / "research_summary.md"
    save_text(summary_file, summary)

    # ── Write RCA events log (after all file writes succeed) ──────────────────
    _write_rca(output_dir, keyword, slug, outcome="success")

    # ── Done ───────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Research complete — {keyword} [{label}]")
    print(f"{'='*60}")
    print(f"  Output folder: {output_dir}")
    print()
    print(f"  Files saved:")
    for f in sorted(output_dir.iterdir()):
        size_kb = round(f.stat().st_size / 1024, 1)
        print(f"    {f.name:<45} {size_kb:>6} KB")
    print()
    print(f"{'='*60}\n")


def _write_rca(output_dir: Path, keyword: str, slug: str, outcome: str) -> None:
    """Write rca_events.json to output_dir with all accumulated events from _thread_context."""
    events: list = getattr(_thread_context, "events", [])
    error_count = sum(1 for e in events if e["level"] == "ERROR")
    warn_count  = sum(1 for e in events if e["level"] == "WARN")
    info_count  = sum(1 for e in events if e["level"] == "INFO")
    rca = {
        "keyword":     keyword,
        "slug":        slug,
        "started_at":  getattr(_thread_context, "started_at", ""),
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "outcome":     outcome,
        "error_count": error_count,
        "warn_count":  warn_count,
        "info_count":  info_count,
        "events":      events,
    }
    save_json(output_dir / "rca_events.json", rca)
    _log("INFO", f"RCA log → rca_events.json (outcome={outcome}, errors={error_count}, warnings={warn_count})", step="rca_write")


def _research_worker(args: tuple) -> tuple:
    """Thread worker — calls run_research_for_keyword and returns (keyword, success)."""
    keyword, is_seed = args
    kw_slug = slugify(keyword)
    try:
        run_research_for_keyword(keyword, is_seed=is_seed)
        return (keyword, True)
    except BaseException as e:
        tb = traceback.format_exc()
        # Ensure thread context has slug so _log and _write_rca work correctly
        if not getattr(_thread_context, "slug", ""):
            _thread_context.slug = kw_slug
        if not getattr(_thread_context, "events", None):
            _thread_context.events = []
        if not getattr(_thread_context, "started_at", ""):
            _thread_context.started_at = datetime.now().isoformat(timespec="seconds")
        _log("ERROR", f"'{keyword}' worker failed: {e}", step="research_worker")
        if tb and tb.strip() not in ("", "NoneType: None"):
            print(tb, flush=True)
        # Persist events to rca_events.json even on hard failure
        output_dir = RESULTS_DIR / kw_slug
        output_dir.mkdir(parents=True, exist_ok=True)
        _write_rca(output_dir, keyword, kw_slug, outcome="failed")
        return (keyword, False)


def run_parallel(keywords: list, batch_size: int):
    """
    Run research for all keywords in batches of `batch_size`, each keyword
    in its own thread (and therefore its own Chromium instance + profile).
    """
    total = len(keywords)
    jobs = [(kw, (i == 0)) for i, kw in enumerate(keywords)]

    completed = []
    failed = []

    for batch_start in range(0, total, batch_size):
        batch = jobs[batch_start: batch_start + batch_size]
        batch_num = batch_start // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size

        print(f"\n{'='*60}")
        print(f"  Batch {batch_num} of {total_batches} — {len(batch)} keyword(s) running in parallel")
        for kw, is_seed in batch:
            label = "SEED" if is_seed else "CLUSTER"
            print(f"    [{label}] {kw}")
        print(f"{'='*60}")

        with ThreadPoolExecutor(max_workers=len(batch)) as executor:
            futures = {executor.submit(_research_worker, job): job[0] for job in batch}
            for future in as_completed(futures):
                kw, success = future.result()
                if success:
                    completed.append(kw)
                else:
                    failed.append(kw)

    print(f"\n{'='*60}")
    print(f"  Parallel research complete — {len(completed)}/{total} succeeded")
    for kw in completed:
        print(f"  ✓  research/{slugify(kw)}/")
    for kw in failed:
        print(f"  ✗  '{kw}' failed — check output above")
    print(f"{'='*60}\n")


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        print("Usage: python tools/serp_research.py [--parallel N] \"seed keyword\" [\"cluster keyword 1\"] ...")
        sys.exit(1)

    # ── Parse --parallel flag ─────────────────────────────────────────────────
    parallel = False
    batch_size = 3

    if "--parallel" in args:
        idx = args.index("--parallel")
        parallel = True
        args.pop(idx)  # remove flag
        if idx < len(args) and args[idx].isdigit():
            batch_size = int(args.pop(idx))

    if not args:
        print("  ERROR: No keywords provided.")
        sys.exit(1)

    keywords = args
    seed = keywords[0]
    clusters = keywords[1:]
    total = len(keywords)

    print(f"\n  Keywords to research : {total} (1 seed + {len(clusters)} cluster{'s' if len(clusters) != 1 else ''})")
    print(f"  Mode                 : {'parallel (batch size ' + str(batch_size) + ')' if parallel else 'sequential'}")
    for i, kw in enumerate(keywords):
        label = "SEED" if i == 0 else f"CLUSTER {i}"
        print(f"  {label}: {kw}")

    if parallel:
        run_parallel(keywords, batch_size)
    else:
        run_research_for_keyword(seed, is_seed=True)
        for cluster in clusters:
            run_research_for_keyword(cluster, is_seed=False)

        if clusters:
            print(f"\n{'='*60}")
            print(f"  All {total} keyword(s) researched.")
            print(f"  Seed folder    : research/{slugify(seed)}/")
            for i, c in enumerate(clusters, 1):
                print(f"  Cluster {i} folder: research/{slugify(c)}/")
            print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
