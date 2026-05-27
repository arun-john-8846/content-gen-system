#!/usr/bin/env python3
"""Quick test: launch Playwright Chromium with research profile."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os, time

BROWSER_PROFILE_PATH = str(Path(os.path.expanduser("~")) / ".playwright-research-profile")
Path(BROWSER_PROFILE_PATH).mkdir(parents=True, exist_ok=True)
print(f"Profile: {BROWSER_PROFILE_PATH}")

with sync_playwright() as p:
    try:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=BROWSER_PROFILE_PATH,
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
        print("SUCCESS: Browser launched")
        time.sleep(2)
        browser.close()
        print("SUCCESS: Browser closed cleanly")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
