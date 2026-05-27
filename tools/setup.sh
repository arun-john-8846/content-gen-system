#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# setup.sh — One-time setup for the SERP research tool
# Run this once before using serp_research.py
# ─────────────────────────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "============================================================"
echo "  SERP Research Tool — Setup"
echo "============================================================"

# ── Check Python ──────────────────────────────────────────────────────────────
echo ""
echo "Checking Python..."
if ! command -v python3 &>/dev/null; then
    echo "  ❌ Python 3 not found. Install from https://python.org"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "  ✓ $PYTHON_VERSION"

# ── Install Playwright Python package ─────────────────────────────────────────
echo ""
echo "Installing Playwright..."
pip3 install -r "$SCRIPT_DIR/requirements.txt" --quiet
echo "  ✓ Playwright installed"

# ── Install Chrome browser for Playwright ─────────────────────────────────────
# Note: For Option C we use your real Chrome, not Playwright's Chromium.
# We still install chromium as a fallback driver.
echo ""
echo "Installing Playwright browser drivers..."
python3 -m playwright install chrome 2>/dev/null || python3 -m playwright install chromium
echo "  ✓ Browser drivers installed"

# ── Create research output folder ─────────────────────────────────────────────
mkdir -p "$SCRIPT_DIR/../research"
echo ""
echo "  ✓ research/ output folder created"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
echo "  Setup complete!"
echo "============================================================"
echo ""
echo "  To run a SERP research session:"
echo ""
echo "    1. Close Chrome completely"
echo "    2. Connect to the VPN for your target locale"
echo "    3. Run:"
echo "       python3 tools/serp_research.py \"file server auditing\""
echo ""
