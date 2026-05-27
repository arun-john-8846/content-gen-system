#!/usr/bin/env python3
"""
Deep content QA across all 44 publish.md files.
Checks: em dashes, style violations, product boundary errors, structural rules,
meta lengths, capability card word counts, paragraph length, and more.
"""
import os, re

pages_dir = "output"
slugs = sorted([
    d for d in os.listdir(pages_dir)
    if os.path.isdir(os.path.join(pages_dir, d))
    and os.path.exists(os.path.join(pages_dir, d, f"{d}_publish.md"))
])

all_issues = {}

def add(issues, slug, category, line_no, text):
    all_issues.setdefault(slug, []).append(f"L{line_no} [{category}] {text[:110]}")

for slug in slugs:
    path = os.path.join(pages_dir, slug, f"{slug}_publish.md")
    content = open(path).read()
    lines = content.splitlines()

    # Locate body start: prefer ## PAGE CONTENT marker; fall back to first H1
    body_start = 0
    _found_body = False
    for i, line in enumerate(lines):
        if re.match(r'^## (?:page content|PAGE CONTENT)', line, re.IGNORECASE):
            body_start = i
            _found_body = True
            break
    if not _found_body:
        for i, line in enumerate(lines):
            if re.match(r'^# [A-Z]', line):
                body_start = i
                break
    body_lines = lines[body_start:]
    body_text = "\n".join(body_lines)

    # Locate FAQ start index in body_lines
    faq_start_in_body = None
    for i, line in enumerate(body_lines):
        if re.match(r'^## (?:FAQ|Frequently asked questions)', line, re.IGNORECASE):
            faq_start_in_body = i
            break

    # Body-only (exclude FAQ for some checks)
    body_no_faq = "\n".join(body_lines[:faq_start_in_body]) if faq_start_in_body else body_text

    # ── 1. EM DASHES ────────────────────────────────────────────────────────
    # Exclude screenshot placeholder lines (editorial notes, not body copy)
    for i, line in enumerate(body_lines, body_start + 1):
        if "—" in line and not line.strip().startswith("ADD SCREENSHOT HERE"):
            add(all_issues, slug, "EM DASH", i, line.strip())

    # ── 2. STYLE: on-prem (not on-premises) ─────────────────────────────────
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\bon-prem\b(?!ises)', line, re.IGNORECASE):
            add(all_issues, slug, "STYLE on-prem", i, line.strip())

    # ── 3. STYLE: "MS " abbreviation for Microsoft ──────────────────────────
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\bMS\s+(Active Directory|AD|Azure|Entra|Office|365|Exchange|Windows|Server)', line):
            add(all_issues, slug, "STYLE MS-abbrev", i, line.strip())

    # ── 4. STYLE: Azure AD alone (post-rebrand) ──────────────────────────────
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\bAzure AD\b', line) and "previously known as Azure AD" not in line and "Azure Active Directory (Azure AD)" not in line:
            add(all_issues, slug, "STYLE Azure-AD", i, line.strip())

    # ── 5. STYLE: email ID / mail ID ────────────────────────────────────────
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\bemail\s+ID\b|\bmail\s+ID\b', line, re.IGNORECASE):
            add(all_issues, slug, "STYLE email-ID", i, line.strip())

    # ── 6. PRODUCT: MITRE ATT&CK in output ──────────────────────────────────
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'MITRE\s+ATT&CK|MITRE ATT', line):
            add(all_issues, slug, "PRODUCT MITRE", i, line.strip())

    # ── 7. PRODUCT: 200+ reports (should be 300+) ───────────────────────────
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'200\+\s*(?:pre-?configured|built-in|reports)', line, re.IGNORECASE):
            add(all_issues, slug, "PRODUCT 200+rpts", i, line.strip())

    # ── 8. PRODUCT: DataSecurity Plus features attributed to ADAP ────────────
    dsp_terms = ["GDPR File Deletion", "GDPR File Access Denied on Sensitive Shares",
                 "content-level data classification", "PII detection", "PHI detection"]
    # Negation prefixes — lines explicitly excluding these features are correct product
    # boundary statements, not violations.
    _dsp_negations = re.compile(
        r'\b(without|does not (include|support|provide|cover)|no |not )\b', re.IGNORECASE)
    for i, line in enumerate(body_lines, body_start + 1):
        for term in dsp_terms:
            if term.lower() in line.lower():
                # Find position of the term and check if a negation appears before it
                term_pos = line.lower().find(term.lower())
                before = line[:term_pos]
                if not _dsp_negations.search(before):
                    add(all_issues, slug, "PRODUCT DSP-boundary", i, line.strip())

    # ── 9. STRUCTURE: H3 in body (not in FAQ, not in meta block) ─────────────
    for i, line in enumerate(body_lines[:faq_start_in_body] if faq_start_in_body else body_lines, body_start + 1):
        if re.match(r'^### ', line):
            add(all_issues, slug, "STRUCT H3-in-body", i, line.strip())

    # ── 10. STRUCTURE: Paragraph > 3 sentences (rough check) ─────────────────
    # Split body (no FAQ) into paragraphs and count sentences per paragraph
    paragraphs = re.split(r'\n\s*\n', body_no_faq)
    para_line_offset = body_start + 1
    for para in paragraphs:
        stripped = para.strip()
        # Only check prose paragraphs (not headings, bullets, cards, tables)
        if not stripped or re.match(r'^[#*|\-\[]', stripped):
            para_line_offset += len(para.splitlines()) + 1
            continue
        # Count sentences (rough: ends with . ? ! followed by space or end)
        sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z])', stripped)
        if len(sentences) > 3:
            first_80 = stripped[:80]
            # Find approximate line number
            for idx, l in enumerate(lines[body_start:para_line_offset+5], body_start+1):
                if stripped[:40] in l:
                    add(all_issues, slug, f"STRUCT {len(sentences)}-sentence-para", idx, stripped[:80])
                    break
        para_line_offset += len(para.splitlines()) + 1

    # ── 11. STRUCTURE: Capability card body > 35 words ────────────────────────
    card_pattern = re.compile(r'^\*\*(?:Card|Benefit card|Capability card) \d+[^*]*\*\*\s*\n(.*?)(?=\n\*\*(?:Card|Benefit card|Capability card) \d+|\n---|\n##|\Z)', re.MULTILINE | re.DOTALL)
    for m in card_pattern.finditer(body_no_faq):
        card_body = m.group(1).strip()
        wc = len(card_body.split())
        if wc > 35:
            # Find line number of card title
            card_title_line = m.group(0).splitlines()[0][:60]
            for idx, l in enumerate(lines[body_start:], body_start + 1):
                if card_title_line[:40] in l:
                    add(all_issues, slug, f"CARD {wc}w>35", idx, l.strip()[:80])
                    break
        if wc < 10 and card_body:
            for idx, l in enumerate(lines[body_start:], body_start + 1):
                if m.group(0).splitlines()[0][:40] in l:
                    add(all_issues, slug, f"CARD {wc}w<10 (empty?)", idx, l.strip()[:80])
                    break

    # ── 12. META: title variant > 60 chars ───────────────────────────────────
    # Lines are formatted: "Meta title A (NN characters): [title text]"
    # Measure only the title text after the colon, not the full label line.
    for i, line in enumerate(lines[:body_start], 1):
        m = re.match(r'^Meta title [ABC] \(\d+ characters\):\s*(.+)$', line.strip(), re.IGNORECASE)
        if m:
            title_text = m.group(1).strip()
            if len(title_text) > 60:
                add(all_issues, slug, f"META title {len(title_text)}ch>60", i, title_text)

    # ── 13. META: description variant > 160 or < 150 chars ───────────────────
    in_meta_desc = False
    for i, line in enumerate(lines[:body_start], 1):
        if re.match(r'^## Meta description', line, re.IGNORECASE):
            in_meta_desc = True
        if not in_meta_desc:
            continue
        stripped = line.strip()
        # Description lines: long prose, no # or *, not a label line
        if (len(stripped) > 80 and not stripped.startswith('#')
                and not stripped.startswith('*') and not stripped.startswith('(')):
            if len(stripped) > 160:
                add(all_issues, slug, f"META desc {len(stripped)}ch>160", i, stripped[:80])
            elif len(stripped) < 150:
                add(all_issues, slug, f"META desc {len(stripped)}ch<150", i, stripped[:80])

    # ── 14. STYLE: rhetorical opener patterns ────────────────────────────────
    rhetorical = [
        r'^In (this|today\'s|an|a) (era|world|environment|section|article)',
        r'^(This|The following) (section|article|page|guide)',
        r'^When it comes to',
        r'^It (is|can be|goes without saying)',
        r'^As (we|you|organizations|businesses)',
    ]
    for i, line in enumerate(body_lines[:faq_start_in_body] if faq_start_in_body else body_lines, body_start + 1):
        for pat in rhetorical:
            if re.match(pat, line.strip(), re.IGNORECASE):
                add(all_issues, slug, "STYLE rhetorical-opener", i, line.strip()[:90])

    # ── 15. STYLE: "PCI DSS" without hyphen ──────────────────────────────────
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\bPCI\s+DSS\b(?!-)', line):
            add(all_issues, slug, "STYLE PCI-DSS", i, line.strip()[:80])

    # ── 16. STYLE: "ISO27001" without space ──────────────────────────────────
    for i, line in enumerate(body_lines, body_start + 1):
        if re.search(r'\bISO27001\b', line):
            add(all_issues, slug, "STYLE ISO27001", i, line.strip()[:80])

    # ── 17. TRUNCATED BODY: very short sections (under 20 words between two H2s) ──
    h2_splits = re.split(r'^(## .+)$', body_no_faq, flags=re.MULTILINE)
    for k in range(1, len(h2_splits) - 1, 2):
        h2_title = h2_splits[k]
        section_body = h2_splits[k + 1].strip()
        wc = len(section_body.split())
        if wc < 20 and wc > 0 and not re.match(r'^## (?:meta|page content)', h2_title, re.IGNORECASE):
            for idx, l in enumerate(lines[body_start:], body_start + 1):
                if h2_title.strip() in l:
                    add(all_issues, slug, f"STRUCT short-section {wc}w", idx, h2_title.strip()[:80])
                    break

print(f"\n{'='*65}")
print(f"DEEP CONTENT QA — {len(slugs)} pages")
print(f"{'='*65}")

total_issues = sum(len(v) for v in all_issues.values())
print(f"\nPages with issues: {len(all_issues)}/{len(slugs)}  |  Total flags: {total_issues}\n")

# Group by category for summary
from collections import Counter
cat_counts = Counter()
for items in all_issues.values():
    for item in items:
        cat = re.search(r'\[([^\]]+)\]', item)
        if cat:
            cat_counts[cat.group(1)] += 1

print("── Summary by category ──────────────────────────────────────")
for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
    print(f"  {cat:<35} {count}")

print("\n── Detail by page ───────────────────────────────────────────")
for slug, items in all_issues.items():
    print(f"\n  {slug}:")
    for item in items:
        print(f"    {item}")

if not all_issues:
    print("\nPASS: No issues found across all 44 pages.")
