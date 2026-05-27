#!/usr/bin/env python3
"""Flow check: verifies page structure rules across all publish.md files."""

import os
import re

pages_dir = "output"
issues = []

slugs = sorted([
    d for d in os.listdir(pages_dir)
    if os.path.isdir(os.path.join(pages_dir, d)) and d != "output"
])

checks = {
    "has_compelling_reasons": 0,
    "has_faq": 0,
    "correct_order": 0,
    "no_benefit_card_grid": 0,
    "no_h3_in_body": 0,
    "faq_count_ok": 0,
    "no_extra_h2_between_cta_and_compelling": 0,
}

for slug in slugs:
    path = os.path.join(pages_dir, slug, f"{slug}_publish.md")
    if not os.path.exists(path):
        print(f"  NOTE: {slug}/ exists but has no _publish.md (skipped)")
        continue

    with open(path, "r") as f:
        content = f.read()

    # Check 1: has compelling reasons
    has_cr = bool(re.search(r'## 4 compelling reasons', content, re.IGNORECASE))
    if not has_cr:
        issues.append(f"{slug}: missing '4 compelling reasons' section")
    else:
        checks["has_compelling_reasons"] += 1

    # Check 2: has FAQ
    has_faq = "## FAQ" in content or "## Frequently asked questions" in content
    if not has_faq:
        issues.append(f"{slug}: missing FAQ section")
    else:
        checks["has_faq"] += 1

    # Check 3: correct order — CTA before compelling reasons before FAQ
    cr_pos = content.find("## 4 compelling reasons")
    faq_pos = max(content.find("## FAQ"), content.find("## Frequently asked questions"))
    # Accept any bracket-style CTA link: [Schedule a...demo], [Download...trial...], etc.
    cta_candidates = [m.start() for m in re.finditer(r'\[(?:Schedule|Download)[^\]]+(?:demo|trial)[^\]]*\]', content, re.IGNORECASE) if m.start() < cr_pos] if cr_pos > 0 else []
    cta_pos = cta_candidates[-1] if cta_candidates else -1
    if cr_pos > 0 and faq_pos > cr_pos and cta_pos > 0 and cta_pos < cr_pos:
        checks["correct_order"] += 1
    else:
        issues.append(f"{slug}: section order wrong (expected CTA -> compelling -> FAQ)")

    # Check 4: no benefit card grid after first CTA
    after_cta = content[cta_pos:] if cta_pos > 0 else content
    if re.search(r'\*\*Benefit card \d+', after_cta):
        issues.append(f"{slug}: second 'Benefit card' grid found after bottom CTA")
    else:
        checks["no_benefit_card_grid"] += 1

    # Check 5: no H3 in body (before compelling reasons)
    body = content[:cr_pos] if cr_pos > 0 else content
    h3_matches = re.findall(r'^### .+', body, re.MULTILINE)
    if h3_matches:
        issues.append(f"{slug}: H3s in body: {h3_matches[:3]}")
    else:
        checks["no_h3_in_body"] += 1

    # Check 6: FAQ count 5-6
    faq_section = content[faq_pos:] if faq_pos > 0 else ""
    faq_h3 = len(re.findall(r'^### ', faq_section, re.MULTILINE))
    faq_bold_q = len(re.findall(r'^\*\*[A-Z]', faq_section, re.MULTILINE))
    q_count = faq_h3 if faq_h3 > 0 else faq_bold_q
    if 5 <= q_count <= 6:
        checks["faq_count_ok"] += 1
    else:
        issues.append(f"{slug}: FAQ has {q_count} questions (expected 5-6)")

    # Check 7: no extra H2 between last CTA and compelling reasons
    if cr_pos > 0 and cta_pos > 0:
        between = content[cta_pos:cr_pos]
        extra_h2 = re.findall(r'^## .+', between, re.MULTILINE)
        if extra_h2:
            issues.append(f"{slug}: extra H2 between CTA and compelling reasons: {extra_h2}")
        else:
            checks["no_extra_h2_between_cta_and_compelling"] += 1
    else:
        checks["no_extra_h2_between_cta_and_compelling"] += 1

total = len([s for s in slugs if os.path.exists(os.path.join(pages_dir, s, f"{s}_publish.md"))])
print(f"Pages checked: {total}\n")
print("CHECK RESULTS:")
for k, v in checks.items():
    status = "PASS" if v == total else f"FAIL ({total - v} failures)"
    print(f"  {k}: {v}/{total} -- {status}")

print(f"\nISSUES FOUND: {len(issues)}")
for issue in issues:
    print(f"  FAIL: {issue}")

if not issues:
    print("  PASS: All checks passed -- all pages clean")
