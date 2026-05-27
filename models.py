"""SQLite schema and CRUD helpers for the ADAP workflow web app."""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

# Allow DATABASE_PATH env override for cloud deployment (Fly.io persistent volume)
_db_env = os.environ.get("DATABASE_PATH")
DB_PATH = Path(_db_env) if _db_env else Path(__file__).parent / "adap.db"
PROJECT_ROOT = Path(__file__).parent


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS pages (
        slug             TEXT PRIMARY KEY,
        seed_keyword     TEXT,
        cluster_1        TEXT DEFAULT '',
        cluster_2        TEXT DEFAULT '',
        cluster_keywords TEXT DEFAULT '[]',
        created_at       TEXT,
        notes            TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS jobs (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        slug        TEXT,
        kind        TEXT,
        status      TEXT,
        started_at  TEXT,
        finished_at TEXT,
        log_path    TEXT,
        pid         INTEGER,
        FOREIGN KEY(slug) REFERENCES pages(slug)
    );

    CREATE TABLE IF NOT EXISTS step_events (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        slug         TEXT,
        step_number  INTEGER,
        event        TEXT,
        ts           TEXT,
        payload_json TEXT,
        FOREIGN KEY(slug) REFERENCES pages(slug)
    );

    CREATE TABLE IF NOT EXISTS settings (
        key   TEXT PRIMARY KEY,
        value TEXT NOT NULL DEFAULT ''
    );
    """)
    conn.commit()
    conn.close()


def scan_filesystem():
    """Scan output/* folders and hydrate pages rows for any not in DB."""
    output_dir = PROJECT_ROOT / "output"
    if not output_dir.exists():
        return
    conn = get_db()
    for folder in output_dir.iterdir():
        if not folder.is_dir():
            continue
        slug = folder.name
        existing = conn.execute(
            "SELECT slug FROM pages WHERE slug=?", (slug,)
        ).fetchone()
        if not existing:
            seed = slug.replace("-", " ")
            conn.execute(
                "INSERT INTO pages(slug, seed_keyword, cluster_1, cluster_2, created_at) "
                "VALUES (?,?,?,?,?)",
                (slug, seed, "", "", datetime.utcnow().isoformat())
            )
    conn.commit()
    conn.close()


# ── Pages ────────────────────────────────────────────────────────────────────

def get_all_pages():
    conn = get_db()
    rows = conn.execute("SELECT * FROM pages ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_page(slug):
    conn = get_db()
    row = conn.execute("SELECT * FROM pages WHERE slug=?", (slug,)).fetchone()
    conn.close()
    return dict(row) if row else None


def insert_page(slug, seed_keyword, cluster_keywords: list):
    conn = get_db()
    conn.execute(
        "INSERT OR IGNORE INTO pages(slug, seed_keyword, cluster_keywords, created_at) "
        "VALUES (?,?,?,?)",
        (slug, seed_keyword, json.dumps(cluster_keywords), datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()


def update_page_clusters(slug, cluster_keywords: list):
    conn = get_db()
    conn.execute(
        "UPDATE pages SET cluster_keywords=? WHERE slug=?",
        (json.dumps(cluster_keywords), slug)
    )
    conn.commit()
    conn.close()


def get_cluster_keywords(page: dict) -> list:
    """Return cluster keywords list for a page dict."""
    raw = page.get("cluster_keywords")
    if raw:
        try:
            kws = json.loads(raw)
            if isinstance(kws, list) and kws:
                return [k for k in kws if k and k.strip()]
        except Exception:
            pass
    # Fallback to legacy columns
    out = []
    for col in ("cluster_1", "cluster_2"):
        v = page.get(col, "")
        if v and v.strip():
            out.append(v.strip())
    return out


# ── Jobs ─────────────────────────────────────────────────────────────────────

def insert_job(slug, kind, log_path, pid):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO jobs(slug, kind, status, started_at, log_path, pid) "
        "VALUES (?,?,?,?,?,?)",
        (slug, kind, "running", datetime.utcnow().isoformat(), log_path, pid)
    )
    job_id = cur.lastrowid
    conn.commit()
    conn.close()
    return job_id


def update_job_status(job_id, status):
    conn = get_db()
    finished = datetime.utcnow().isoformat() if status in ("done", "error") else None
    conn.execute(
        "UPDATE jobs SET status=?, finished_at=? WHERE id=?",
        (status, finished, job_id)
    )
    conn.commit()
    conn.close()


def get_latest_job(slug, kind):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM jobs WHERE slug=? AND kind=? ORDER BY id DESC LIMIT 1",
        (slug, kind)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_job_by_id(job_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ── Step events ───────────────────────────────────────────────────────────────

def add_step_event(slug, step_number, event, payload=None):
    payload_json = json.dumps(payload) if payload is not None else None
    conn = get_db()
    conn.execute(
        "INSERT INTO step_events(slug, step_number, event, ts, payload_json) "
        "VALUES (?,?,?,?,?)",
        (slug, step_number, event, datetime.utcnow().isoformat(), payload_json)
    )
    conn.commit()
    conn.close()


def get_step_events(slug):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM step_events WHERE slug=? ORDER BY ts ASC", (slug,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def has_event(slug, event):
    conn = get_db()
    row = conn.execute(
        "SELECT id FROM step_events WHERE slug=? AND event=? LIMIT 1",
        (slug, event)
    ).fetchone()
    conn.close()
    return row is not None


def get_latest_event(slug, event):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM step_events WHERE slug=? AND event=? ORDER BY id DESC LIMIT 1",
        (slug, event)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ── Settings (key/value store) ────────────────────────────────────────────────

def get_setting(key: str, default: str = "") -> str:
    """Read a setting from DB. Returns default if not set."""
    conn = get_db()
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    """Upsert a setting in the DB."""
    conn = get_db()
    conn.execute(
        "INSERT INTO settings(key, value) VALUES (?,?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value)
    )
    conn.commit()
    conn.close()


def get_all_settings() -> dict:
    """Return all settings as a dict."""
    conn = get_db()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return {r["key"]: r["value"] for r in rows}
