"""Subprocess runners and log helpers for the ADAP workflow web app."""

import os
import re
import sys
import subprocess
import threading
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
LOGS_DIR = PROJECT_ROOT / "logs"

# Keep proc references in memory so we can send stdin (lost on restart — acceptable for v1)
RUNNING_PROCS = {}  # job_id -> proc


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def ensure_logs_dir():
    LOGS_DIR.mkdir(exist_ok=True)


def is_process_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, OSError):
        return False


# ── Research job ─────────────────────────────────────────────────────────────

def run_research(slug: str, seed_keyword: str, cluster_keywords: list, batch_size: int = 3) -> int:
    """Spawn serp_research.py as a subprocess. Returns job_id."""
    import time
    from models import insert_job, update_job_status

    ensure_logs_dir()
    log_name = f"research_{slug}_{int(time.time())}.log"
    log_path = str(LOGS_DIR / log_name)

    has_clusters = any(kw.strip() for kw in (cluster_keywords or []))
    args = [sys.executable, str(PROJECT_ROOT / "tools" / "serp_research.py")]
    if has_clusters:
        args += ["--parallel", str(max(1, min(int(batch_size), 5)))]
    args.append(seed_keyword)
    for kw in (cluster_keywords or []):
        if kw.strip():
            args.append(kw.strip())

    log_file = open(log_path, "w", buffering=1)
    proc = subprocess.Popen(
        args,
        cwd=str(PROJECT_ROOT),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
    )

    job_id = insert_job(slug, "research", log_path, proc.pid)
    RUNNING_PROCS[job_id] = proc

    def _monitor():
        proc.wait()
        try:
            log_file.close()
        except Exception:
            pass
        status = "done" if proc.returncode == 0 else "error"
        update_job_status(job_id, status)
        RUNNING_PROCS.pop(job_id, None)

    threading.Thread(target=_monitor, daemon=True).start()
    return job_id


def send_captcha_enter(job_id: int) -> bool:
    """Send newline to unblock input() in the subprocess after CAPTCHA solve."""
    proc = RUNNING_PROCS.get(job_id)
    if proc and proc.stdin:
        try:
            proc.stdin.write("\n")
            proc.stdin.flush()
            return True
        except (BrokenPipeError, OSError):
            return False
    return False


def get_research_status(job_id: int, log_path: str) -> str:
    """Return 'running', 'done', or 'error' for a research job."""
    from models import get_job_by_id

    if job_id in RUNNING_PROCS:
        proc = RUNNING_PROCS[job_id]
        if proc.poll() is None:
            return "running"
        return "done" if proc.returncode == 0 else "error"

    # Server restarted — proc reference lost; fall back to process alive check + DB
    job = get_job_by_id(job_id)
    if not job:
        return "unknown"
    if job["status"] != "running":
        return job["status"]
    if job["pid"] and is_process_alive(job["pid"]):
        return "running"
    try:
        with open(log_path, "r") as f:
            content = f.read()
        if "Research complete" in content or "Summary saved" in content:
            return "done"
    except FileNotFoundError:
        pass
    return "error"


def read_log_chunk(log_path: str, since_bytes: int = 0):
    """Read new content from a log file from byte offset. Returns (text, new_offset)."""
    try:
        with open(log_path, "rb") as f:
            f.seek(since_bytes)
            raw = f.read()
        text = raw.decode("utf-8", errors="replace")
        return text, since_bytes + len(raw)
    except FileNotFoundError:
        return "", since_bytes


def has_captcha_prompt(text: str) -> bool:
    return "CAPTCHA detected" in text or "solve it in the Chrome window" in text


# ── QA job ───────────────────────────────────────────────────────────────────

def run_qa(slug: str):
    """Run qa_check.py against the draft. Returns (stdout_str, returncode)."""
    draft_path = PROJECT_ROOT / "output" / slug / f"{slug}_draft.md"
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "tools" / "qa_check.py"), str(draft_path)],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    return result.stdout + result.stderr, result.returncode


# ── Build docx job ────────────────────────────────────────────────────────────

def run_build(slug: str):
    """Run build_docx.py for a slug. Returns (stdout_str, returncode)."""
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "tools" / "build_docx.py"), slug],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    return result.stdout + result.stderr, result.returncode
