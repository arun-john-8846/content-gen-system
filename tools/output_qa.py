#!/usr/bin/env python3
"""Output quality check: annotations, empty cards, gibberish markers in body."""
import os, re

pages_dir = "output"
issues = {}

for slug in sorted(os.listdir(pages_dir)):
    path = os.path.join(pages_dir, slug, f"{slug}_publish.md")
    if not os.path.exists(path):
        continue
    lines = open(path).readlines()
    content = "".join(lines)

    page_issues = []

    # Locate start of page body (after ## Page content / ## PAGE CONTENT)
    body_start = 0
    for i, line in enumerate(lines):
        if re.match(r'^## (?:page content|PAGE CONTENT)', line, re.IGNORECASE):
            body_start = i
            break

    body_lines = lines[body_start:]

    # Check 1: *(centred)* or *(centered)* annotations in body
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\*\(centred\)\*|\*\(centered\)\*', line):
            page_issues.append(f"L{i} [ANNOTATION] *(centred)* in body: {line.strip()[:80]}")

    # Check 2: *(N characters)* char-count markers in body
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\*\(\d+ characters\)\*', line):
            page_issues.append(f"L{i} [ANNOTATION] char-count in body: {line.strip()[:80]}")

    # Check 3: Card title with no body content on next non-blank line
    for i, line in enumerate(lines):
        if re.match(r'^\*\*Card \d+:', line):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines):
                nxt = lines[j].strip()
                if re.match(r'^\*\*Card \d+:|^---|^##', nxt):
                    page_issues.append(f"L{i+1} [EMPTY CARD] no body: {line.strip()[:70]}")

    # Check 4: Benefit card grid heading lines (grid titles) without card content below
    for i, line in enumerate(lines):
        if re.match(r'^\*\*Benefit card [0-9]+', line, re.IGNORECASE):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            if j < len(lines):
                nxt = lines[j].strip()
                if re.match(r'^\*\*Benefit card|^---|^##', nxt):
                    page_issues.append(f"L{i+1} [EMPTY BENEFIT CARD]: {line.strip()[:70]}")

    # Check 5: Orphan link-only lines that look like lone bracketed links (possible build artifact)
    for i, line in enumerate(body_lines, body_start + 1):
        stripped = line.strip()
        if re.match(r'^\[.{5,80}\]\(https?://', stripped) and stripped.endswith(')'):
            page_issues.append(f"L{i} [BARE LINK LINE]: {stripped[:80]}")

    # Check 6: Raw placeholder text
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\[screenshot\]|\[placeholder\]|\[INSERT\]|\[TBD\]|\[TODO\]', line, re.IGNORECASE):
            page_issues.append(f"L{i} [PLACEHOLDER]: {line.strip()[:80]}")

    if page_issues:
        issues[slug] = page_issues

print(f"Pages with output quality issues: {len(issues)}/{len([d for d in os.listdir(pages_dir) if os.path.exists(os.path.join(pages_dir,d,f'{d}_publish.md'))])}\n")
for slug, items in issues.items():
    print(f"\n  {slug}:")
    for item in items:
        print(f"    {item}")

if not issues:
    print("PASS: No annotation leakage, empty cards, or placeholder text found.")
