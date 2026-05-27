#!/usr/bin/env python3
"""
Batch structural fix for ADAudit Plus feature pages.
Applies two automated changes to all publish.md files:
  1. Insert '4 compelling reasons' section before FAQ
  2. Remove MITRE ATT&CK® mentions (replace with product framing)
"""
import re, os, sys

COMPELLING_REASONS = """
---

## 4 compelling reasons to choose ADAudit Plus

**Widely recognized**
ADAudit Plus has been recognized as a Gartner Peer Insights Customers' Choice for Security Incident & Event Management (SIEM) for four consecutive years.

**Easy deployment**
Go from downloading ADAudit Plus to receiving predefined reports and alerts in under 30 minutes, without any professional services engagement.

**Competitive pricing**
ADAudit Plus is licensed per-server, not per-user. As your user count grows, you continue to ingest log data without additional licensing costs.

**Unified visibility**
ADAudit Plus consolidates auditing, security, and compliance across Active Directory, Microsoft Entra ID, Windows servers, workstations, and file servers into a single console, eliminating the need to manage multiple tools.

"""

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
    if "## 4 compelling reasons to choose ADAudit Plus" not in content:
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
