#!/usr/bin/env python3
"""
Batch structural fix for feature pages.
Applies two automated changes to all publish.md files:
  1. Insert '4 compelling reasons' section before FAQ (reads from reference/compelling_reasons.md)
  2. Remove MITRE ATT&CK® mentions (replace with product framing)
"""
import re, os, sys

COMPELLING_REASONS_FILE = os.path.join(os.path.dirname(__file__), "..", "reference", "compelling_reasons.md")

def _load_compelling_reasons():
    if os.path.isfile(COMPELLING_REASONS_FILE):
        with open(COMPELLING_REASONS_FILE, "r") as f:
            return "\n---\n\n" + f.read().strip() + "\n\n"
    return ""

OUTPUT_DIR = "output"
SKIP_SLUGS = {"employee-time-tracking-software", "windows-server-auditing-software", "output"}

results = []

for slug in sorted(os.listdir(OUTPUT_DIR)):
    if slug in SKIP_SLUGS or slug.startswith("."):
        continue
    md_path = os.path.join(OUTPUT_DIR, slug, f"{slug}_publish.md")
    if not os.path.isfile(md_path):
        results.append(f"SKIP (no file): {slug}")
        continue

    with open(md_path, "r") as f:
        content = f.read()

    original = content
    changed = []

    # 1. Add compelling reasons before FAQ (if not already present)
    COMPELLING_REASONS = _load_compelling_reasons()
    cr_heading_match = re.search(r'^## 4 compelling reasons', content, re.MULTILINE | re.IGNORECASE)
    if not cr_heading_match and COMPELLING_REASONS:
        # Find the FAQ heading and insert before it
        faq_match = re.search(r'\n## Frequently asked questions', content)
        if faq_match:
            pos = faq_match.start()
            content = content[:pos] + COMPELLING_REASONS + content[pos:]
            changed.append("added compelling reasons")
        else:
            results.append(f"WARN (no FAQ found): {slug}")

    # 2. Remove MITRE ATT&CK® and MITRE ATT&CK mentions
    # Pattern: replace whole sentence containing MITRE if it adds no info beyond product framing
    # Safe replacement: remove the MITRE phrase from the sentence
    mitre_patterns = [
        # "using MITRE ATT&CK® framework techniques" at end of sentence
        (r',?\s+using (?:the )?MITRE ATT&CK[®\u00ae]?\s+(?:framework\s+)?(?:techniques?|framework)?', ''),
        # "via MITRE ATT&CK®" 
        (r'\s+via MITRE ATT&CK[®\u00ae]?', ''),
        # "aligned with MITRE ATT&CK®" or "mapped to MITRE ATT&CK®"
        (r',?\s+(?:aligned with|mapped to|based on) MITRE ATT&CK[®\u00ae]?', ''),
        # standalone MITRE ATT&CK® mentions in bullets or sentences
        (r'MITRE ATT&CK[®\u00ae]', 'MITRE ATT\u0026CK'),  # placeholder — catch remaining
    ]

    for pat, repl in mitre_patterns[:-1]:
        new = re.sub(pat, repl, content, flags=re.IGNORECASE)
        if new != content:
            content = new
            changed.append("removed MITRE phrase")

    # Check for remaining MITRE ATT&CK mentions
    remaining_mitre = re.findall(r'MITRE ATT&CK', content, re.IGNORECASE)
    if remaining_mitre:
        changed.append(f"WARNING: {len(remaining_mitre)} MITRE mention(s) remain — manual fix needed")

    if content != original:
        with open(md_path, "w") as f:
            f.write(content)
        results.append(f"UPDATED ({', '.join(changed)}): {slug}")
    else:
        results.append(f"no change: {slug}")

print("\n".join(results))
print(f"\nDone. {len([r for r in results if r.startswith('UPDATED')])} files updated.")
