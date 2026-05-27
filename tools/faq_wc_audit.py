#!/usr/bin/env python3
"""FAQ answer word-count audit. Reports answers outside 40-50 words."""
import os
import re

pages_dir = "output"
slugs = sorted([
    d for d in os.listdir(pages_dir)
    if os.path.isdir(os.path.join(pages_dir, d))
    and os.path.exists(os.path.join(pages_dir, d, f"{d}_publish.md"))
])

all_issues = {}

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
    bold_questions = re.findall(r'^\*\*(.+\?)\*\*\s*$', faq_section, re.MULTILINE)
    h3_questions = re.findall(r'^### (.+)$', faq_section, re.MULTILINE)

    if bold_questions:
        questions = bold_questions
        qa_blocks = re.split(r'^\*\*.+\?\*\*\s*$', faq_section, flags=re.MULTILINE)
    elif h3_questions:
        questions = h3_questions
        qa_blocks = re.split(r'^### .+$', faq_section, flags=re.MULTILINE)
    else:
        continue

    qa_blocks = [b.strip() for b in qa_blocks if b.strip()]
    qa_blocks = [b for b in qa_blocks if not re.match(r'^##', b)]

    page_issues = []
    for i, (q, answer_block) in enumerate(zip(questions, qa_blocks), 1):
        # Strip trailing non-FAQ content (end-of-content markers, HR lines, internal link tables)
        answer_block = re.split(r'\*End of publishable content\*|^---\s*$', answer_block, maxsplit=1, flags=re.MULTILINE)[0]
        answer_text = re.sub(r'^#.*$', '', answer_block, flags=re.MULTILINE).strip()
        wc = len(answer_text.split())
        if wc < 40 or wc > 50:
            status = "SHORT" if wc < 40 else "LONG"
            page_issues.append((i, wc, status, q[:65]))

    if page_issues:
        all_issues[slug] = page_issues

print(f"Pages with FAQ word-count violations: {len(all_issues)}/{len(slugs)}\n")
for slug, items in all_issues.items():
    print(f"  {slug}:")
    for i, wc, status, q in items:
        print(f"    Q{i} [{status} {wc}w]: {q}")

if not all_issues:
    print("PASS: All FAQ answers are 40-50 words.")
