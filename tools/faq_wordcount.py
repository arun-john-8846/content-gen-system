#!/usr/bin/env python3
"""Audit FAQ answer word counts across all publish.md files."""
import os
import re

pages_dir = "output"
slugs = sorted([
    d for d in os.listdir(pages_dir)
    if os.path.isdir(os.path.join(pages_dir, d))
    and os.path.exists(os.path.join(pages_dir, d, f"{d}_publish.md"))
])

violations = {}
clean = []

for slug in slugs:
    path = os.path.join(pages_dir, slug, f"{slug}_publish.md")
    with open(path, "r") as f:
        content = f.read()

    faq_match = re.search(
        r'^## (?:FAQ|Frequently asked questions)\s*$',
        content, re.MULTILINE | re.IGNORECASE
    )
    if not faq_match:
        continue
    faq_section = content[faq_match.start():]

    h3_qs = re.findall(r'^### (.+)$', faq_section, re.MULTILINE)
    bold_qs = re.findall(r'^\*\*(.+\?)\*\*\s*$', faq_section, re.MULTILINE)
    fmt = "h3" if h3_qs else "bold"
    questions = h3_qs if h3_qs else bold_qs

    if fmt == "h3":
        blocks = re.split(r'^### .+$', faq_section, flags=re.MULTILINE)
    else:
        blocks = re.split(r'^\*\*.+\?\*\*\s*$', faq_section, flags=re.MULTILINE)

    answer_blocks = [
        b.strip() for b in blocks
        if b.strip() and not re.match(r'^##', b.strip())
    ]

    page_issues = []
    for i, (q, ab) in enumerate(zip(questions, answer_blocks), 1):
        text = re.sub(r'^#.*$', '', ab, flags=re.MULTILINE).strip()
        wc = len(text.split())
        if wc < 40 or wc > 50:
            status = "OVER" if wc > 50 else "UNDER"
            page_issues.append((i, wc, status, q[:70]))

    if page_issues:
        violations[slug] = page_issues
    else:
        clean.append(slug)

total = len(slugs)
print(f"Pages audited: {total}")
print(f"Clean (all answers 40-50w): {len(clean)}")
print(f"Pages with violations: {len(violations)}\n")

total_fixes = 0
for slug, issues in violations.items():
    print(f"  {slug}:")
    for q_num, wc, status, q in issues:
        print(f"    Q{q_num} [{status}: {wc}w] {q}")
        total_fixes += 1

print(f"\nTotal answers to fix: {total_fixes}")
