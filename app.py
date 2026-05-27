"""Flask app — ADAP Content Gen Web (platform-agnostic version)."""

import json
import os
import re
import sys
import time
from pathlib import Path

from flask import (
    Flask,
    Response,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    stream_with_context,
    url_for,
)

import config
import jobs as job_runner
import models
import pipeline

PROJECT_ROOT = Path(__file__).parent

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.environ.get("SECRET_KEY", "adap-web-dev-2026"))

# Boot: schema + filesystem scan
models.init_db()
models.scan_filesystem()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _get_step_progress(slug: str, page: dict) -> list:
    research_slug = _slugify(page.get("seed_keyword") or slug)
    research_dir = PROJECT_ROOT / "research" / research_slug
    research_done = (research_dir / "research_summary.md").exists()

    latest_research = models.get_latest_job(slug, "research")
    research_running = bool(
        latest_research
        and latest_research["status"] == "running"
        and (
            latest_research["id"] in job_runner.RUNNING_PROCS
            or (latest_research["pid"] and job_runner.is_process_alive(latest_research["pid"]))
        )
    )

    brief_file_exists = (PROJECT_ROOT / "output" / slug / f"{slug}_brief.md").exists()
    brief_approved = brief_file_exists
    draft_done = (PROJECT_ROOT / "output" / slug / f"{slug}_draft.md").exists()
    qa_done = models.has_event(slug, "qa_ran")
    humanized = models.has_event(slug, "humanized")
    delivery_done = (PROJECT_ROOT / "output" / slug / f"{slug}_publish.docx").exists()

    pipeline_running = pipeline.is_running(slug)

    def _s(done, running=False):
        if done:
            return "done"
        if running:
            return "in-progress"
        return "not-started"

    return [
        {"number": 1, "label": "Research",             "status": _s(research_done, research_running)},
        {"number": 2, "label": "Brief (auto-approved)", "status": _s(brief_approved)},
        {"number": 3, "label": "Draft",                "status": _s(draft_done, pipeline_running and not draft_done)},
        {"number": 4, "label": "QA + Humanize",        "status": _s(qa_done, pipeline_running and draft_done and not qa_done)},
        {"number": 5, "label": "Post-humanization QA", "status": _s(humanized)},
        {"number": 6, "label": "Delivery",             "status": _s(delivery_done, pipeline_running and qa_done and not delivery_done)},
    ]


def _get_research_folders(page: dict) -> list:
    entries = []
    research_dir = PROJECT_ROOT / "research"
    keywords = [("Seed", page.get("seed_keyword", ""))] + [
        (f"Cluster {i+1}", kw)
        for i, kw in enumerate(models.get_cluster_keywords(page))
    ]
    for label, kw in keywords:
        kw_slug = _slugify(kw)
        folder = research_dir / kw_slug
        summary_exists = (folder / "research_summary.md").exists()
        competitor_count = len(list(folder.glob("competitor_*.txt"))) if folder.exists() else 0
        entries.append({
            "label": label,
            "keyword": kw,
            "kw_slug": kw_slug,
            "summary_exists": summary_exists,
            "competitor_count": competitor_count,
        })
    return entries


def _parse_qa_output(output: str):
    sections = []
    lines = output.strip().split("\n")
    current = None

    for line in lines:
        m = re.match(r"^\[(\d+)\]\s+(.+?)(?::\s*(\d+))?$", line)
        if m:
            if current:
                sections.append(current)
            count_str = m.group(3)
            current = {
                "num": int(m.group(1)),
                "label": m.group(2),
                "count": int(count_str) if count_str is not None else None,
                "details": [],
                "status": "pass",
            }
        elif line.startswith("====="):
            if current:
                sections.append(current)
            current = None
        elif current and line.strip():
            current["details"].append(line.strip())

    if current:
        sections.append(current)

    for s in sections:
        if s["count"] is not None and s["count"] > 0:
            s["status"] = "fail"
        for d in s["details"]:
            if "FAIL:" in d or "FOUND:" in d:
                s["status"] = "fail"
            elif "WARNING:" in d and s["status"] == "pass":
                s["status"] = "warn"

    total_m = re.search(r"TOTAL GENUINE ISSUES:\s*(\d+)", output)
    total = int(total_m.group(1)) if total_m else sum(
        1 for s in sections if s["status"] == "fail"
    )
    return sections, total


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    pages = models.get_all_pages()
    page_data = []
    for p in pages:
        steps = _get_step_progress(p["slug"], p)
        page_data.append({"page": p, "steps": steps})
    return render_template("dashboard.html", page_data=page_data)


# ── New page ──────────────────────────────────────────────────────────────────

@app.route("/pages/new", methods=["GET", "POST"])
def new_page():
    if request.method == "POST":
        seed = request.form.get("seed_keyword", "").strip()
        cluster_keywords = [
            v.strip() for k, v in request.form.items()
            if k.startswith("cluster_kw_") and v.strip()
        ]
        slug = request.form.get("slug", "").strip() or _slugify(seed)

        if not seed or not slug:
            flash("Seed keyword and slug are required.", "error")
            return render_template("new_page.html", form=request.form)

        out_dir = PROJECT_ROOT / "output" / slug
        out_dir.mkdir(parents=True, exist_ok=True)

        models.insert_page(slug, seed, cluster_keywords)

        batch_size = max(1, min(int(request.form.get("parallel_batch_size", 3) or 3), 5))
        job_id = job_runner.run_research(slug, seed, cluster_keywords, batch_size=batch_size)
        flash(f"Research started (job {job_id}).", "success")
        return redirect(url_for("page_detail", slug=slug, tab="research"))

    return render_template("new_page.html", form={})


# ── Page detail ───────────────────────────────────────────────────────────────

@app.route("/pages/<slug>")
def page_detail(slug):
    page = models.get_page(slug)
    if not page:
        abort(404)

    active_tab = request.args.get("tab", "overview")
    steps = _get_step_progress(slug, page)
    research_folders = _get_research_folders(page)
    latest_research_job = models.get_latest_job(slug, "research")

    out_dir = PROJECT_ROOT / "output" / slug
    output_files = sorted(out_dir.iterdir()) if out_dir.exists() else []

    qa_event = models.get_latest_event(slug, "qa_ran")
    qa_sections, qa_total = [], 0
    if qa_event and qa_event.get("payload_json"):
        try:
            payload = json.loads(qa_event["payload_json"])
            qa_sections, qa_total = _parse_qa_output(payload.get("output", ""))
        except Exception:
            pass

    publish_docx = out_dir / f"{slug}_publish.docx"
    review_docx = out_dir / f"{slug}_review.docx"

    brief_path = out_dir / f"{slug}_brief.md"
    brief_exists = brief_path.exists()
    brief_html = ""
    brief_raw = ""
    brief_mtime = None
    if brief_exists:
        brief_raw = brief_path.read_text(encoding="utf-8")
        try:
            import markdown as md_lib
            brief_html = md_lib.markdown(brief_raw, extensions=["tables", "fenced_code"])
        except ImportError:
            brief_html = f"<pre>{brief_raw}</pre>"
        try:
            from datetime import datetime as _dt
            brief_mtime = _dt.fromtimestamp(brief_path.stat().st_mtime).isoformat(timespec="seconds")
        except Exception:
            brief_mtime = None

    pipeline_running = pipeline.is_running(slug)
    config_provider = config.get("llm_provider").title()

    return render_template(
        "page_detail.html",
        page=page,
        slug=slug,
        active_tab=active_tab,
        steps=steps,
        research_folders=research_folders,
        latest_research_job=latest_research_job,
        output_files=[f.name for f in output_files if f.is_file()],
        qa_sections=qa_sections,
        qa_total=qa_total,
        qa_ts=qa_event["ts"] if qa_event else None,
        publish_docx_exists=publish_docx.exists(),
        review_docx_exists=review_docx.exists(),
        brief_exists=brief_exists,
        brief_html=brief_html,
        brief_raw=brief_raw,
        brief_mtime=brief_mtime,
        brief_approved=brief_exists,
        cluster_keywords=models.get_cluster_keywords(page),
        pipeline_running=pipeline_running,
        config_provider=config_provider,
    )


# ── Research endpoints ────────────────────────────────────────────────────────

@app.route("/pages/<slug>/research/start", methods=["POST"])
def research_start(slug):
    page = models.get_page(slug)
    if not page:
        abort(404)
    batch_size = max(1, min(int(request.form.get("parallel_batch_size", 3) or 3), 5))
    job_id = job_runner.run_research(
        slug, page["seed_keyword"], models.get_cluster_keywords(page), batch_size=batch_size,
    )
    flash(f"Research re-started (job {job_id}).", "success")
    return redirect(url_for("page_detail", slug=slug, tab="research"))


@app.route("/pages/<slug>/research/log")
def research_log(slug):
    job = models.get_latest_job(slug, "research")
    if not job:
        return jsonify({"text": "", "offset": 0, "status": "none", "captcha": False})
    since = int(request.args.get("since", 0))
    text, new_offset = job_runner.read_log_chunk(job["log_path"], since)
    status = job_runner.get_research_status(job["id"], job["log_path"])
    captcha = job_runner.has_captcha_prompt(text)
    return jsonify({"text": text, "offset": new_offset, "status": status,
                    "captcha": captcha, "job_id": job["id"]})


@app.route("/pages/<slug>/research/captcha-continue", methods=["POST"])
def captcha_continue(slug):
    job = models.get_latest_job(slug, "research")
    if job:
        sent = job_runner.send_captcha_enter(job["id"])
        return jsonify({"ok": sent})
    return jsonify({"ok": False})


@app.route("/pages/<slug>/research/<kw_slug>")
def research_view(slug, kw_slug):
    summary_path = PROJECT_ROOT / "research" / kw_slug / "research_summary.md"
    if not summary_path.exists():
        abort(404)
    try:
        import markdown as md_lib
        content_html = md_lib.markdown(
            summary_path.read_text(encoding="utf-8"),
            extensions=["tables", "fenced_code"],
        )
    except ImportError:
        content_html = f"<pre>{summary_path.read_text(encoding='utf-8')}</pre>"
    page = models.get_page(slug)
    return render_template("research_view.html", page=page, slug=slug,
                           kw_slug=kw_slug, content_html=content_html)


# ── Brief ─────────────────────────────────────────────────────────────────────

@app.route("/pages/<slug>/brief-approve", methods=["POST"])
def brief_approve(slug):
    flash("Brief is auto-approved in fully automated mode.", "info")
    return redirect(url_for("page_detail", slug=slug, tab="brief"))


@app.route("/pages/<slug>/brief-save", methods=["POST"])
def brief_save(slug):
    content = request.form.get("brief_content", "")
    out_dir = PROJECT_ROOT / "output" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{slug}_brief.md").write_text(content, encoding="utf-8")
    flash("Brief saved.", "success")
    return redirect(url_for("page_detail", slug=slug, tab="brief"))


# ── Humanize marker ───────────────────────────────────────────────────────────

@app.route("/pages/<slug>/mark-humanized", methods=["POST"])
def mark_humanized(slug):
    models.add_step_event(slug, 5, "humanized")
    flash("Step 5 (post-humanization QA) marked as complete.", "success")
    return redirect(url_for("page_detail", slug=slug, tab="qa"))


# ── Manual QA runner ──────────────────────────────────────────────────────────

@app.route("/pages/<slug>/qa", methods=["POST"])
def run_qa(slug):
    draft_path = PROJECT_ROOT / "output" / slug / f"{slug}_draft.md"
    if not draft_path.exists():
        flash("Draft file not found. Run the pipeline first.", "error")
        return redirect(url_for("page_detail", slug=slug, tab="qa"))
    output, _ = job_runner.run_qa(slug)
    sections, total = _parse_qa_output(output)
    models.add_step_event(slug, 3, "qa_ran", {"output": output, "total_issues": total})
    flash(f"QA complete — {total} genuine issue(s) found.", "success" if total == 0 else "warning")
    return redirect(url_for("page_detail", slug=slug, tab="qa"))


# ── Manual build .docx ────────────────────────────────────────────────────────

@app.route("/pages/<slug>/build", methods=["POST"])
def build_docx(slug):
    output, returncode = job_runner.run_build(slug)
    if returncode == 0:
        models.add_step_event(slug, 6, "docx_built", {"output": output})
        flash(".docx files built successfully.", "success")
    else:
        flash("Build failed. Check output/logs.", "error")
    return redirect(url_for("page_detail", slug=slug, tab="delivery"))


# ── Pipeline (auto LLM pipeline) ──────────────────────────────────────────────

@app.route("/pages/<slug>/pipeline/start", methods=["POST"])
def pipeline_start(slug):
    page = models.get_page(slug)
    if not page:
        abort(404)

    # Check LLM is configured
    provider = config.get("llm_provider")
    key_field = "anthropic_api_key" if provider == "anthropic" else "openai_api_key"
    if not config.get(key_field):
        flash(
            f"No {provider.title()} API key configured. "
            "Go to Settings and enter your API key before running the pipeline.",
            "error",
        )
        return redirect(url_for("page_detail", slug=slug, tab="overview"))

    started = pipeline.start_pipeline_thread(slug)
    if started:
        flash("Pipeline started. Watch the Pipeline tab for live progress.", "success")
    else:
        flash("Pipeline is already running for this page.", "info")
    return redirect(url_for("page_detail", slug=slug, tab="pipeline"))


@app.route("/pages/<slug>/pipeline/cancel", methods=["POST"])
def pipeline_cancel(slug):
    pipeline.cancel_pipeline(slug)
    flash("Cancel signal sent. The pipeline will stop at the next checkpoint.", "info")
    return redirect(url_for("page_detail", slug=slug, tab="pipeline"))


@app.route("/pages/<slug>/pipeline/status")
def pipeline_status(slug):
    """JSON polling endpoint for pipeline status + new log lines."""
    offset = int(request.args.get("offset", 0))
    new_lines, new_offset = pipeline.get_log_from(slug, offset)
    running = pipeline.is_running(slug)
    return jsonify({"lines": new_lines, "offset": new_offset, "running": running})


@app.route("/pages/<slug>/pipeline/stream")
def pipeline_stream(slug):
    """SSE endpoint that streams pipeline log lines in real time."""
    @stream_with_context
    def _generate():
        offset = 0
        # Allow a bit of headroom — up to 5 minutes of inactivity before we close
        idle_ticks = 0
        while True:
            new_lines, new_offset = pipeline.get_log_from(slug, offset)
            if new_lines:
                idle_ticks = 0
                for line in new_lines:
                    yield f"data: {json.dumps(line)}\n\n"
                offset = new_offset
            else:
                idle_ticks += 1

            running = pipeline.is_running(slug)
            if not running and not new_lines:
                yield "data: __DONE__\n\n"
                break
            if idle_ticks > 300:  # 5 min (300 × 1s)
                yield "data: __TIMEOUT__\n\n"
                break
            time.sleep(1)

    return Response(_generate(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── File download ──────────────────────────────────────────────────────────────

@app.route("/pages/<slug>/files/<filename>")
def serve_file(slug, filename):
    # Prevent directory traversal
    safe_name = Path(filename).name
    file_path = PROJECT_ROOT / "output" / slug / safe_name
    if not file_path.exists() or not file_path.is_file():
        abort(404)
    return send_file(str(file_path), as_attachment=True)


# ── Settings ──────────────────────────────────────────────────────────────────

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        saved = []
        for key in config.KNOWN_KEYS:
            val = request.form.get(key)
            if val is not None:
                # Skip keys that are locked via env vars
                env_name = config._ENV_MAP.get(key)
                if env_name and os.environ.get(env_name):
                    continue
                # Don't overwrite API keys with blank (user left field empty)
                if key.endswith("_api_key") and not val.strip():
                    continue
                config.set(key, val.strip())
                saved.append(key)
        flash(f"Settings saved ({len(saved)} field(s) updated).", "success")
        return redirect(url_for("settings"))

    settings_data = config.get_all_for_ui()
    return render_template("settings.html", settings=settings_data)


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    # Listen on 0.0.0.0 so Docker/Fly.io external traffic reaches the app
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
