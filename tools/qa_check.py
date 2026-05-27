#!/usr/bin/env python3
"""Generic QA checker for content pipeline drafts.

Checks:
  1. Em dashes in body
  2. POV violations (organizations + verb)
  3. Passive voice (was/were Xed by)
  4. AI writing patterns
  5. Paragraph length (>= 4 sentences)
  6. Number rule (single digits in prose)
  7. H3 subheadings in body
  8. Custom BANNED: strings from reference/qa_rules.md

Usage:
  python qa_check.py path/to/draft.md
"""
import re
import sys
from pathlib import Path

filepath = sys.argv[1] if len(sys.argv) > 1 else 'output/draft.md'

with open(filepath, 'r') as f:
    content = f.read()

issues = []

# ── 1. Em dashes in body ──────────────────────────────────────────────────────
# Exclude meta block, table dividers, screenshot placeholders, headings
em_dash_hits = []
in_meta_block = False
for line in content.split('\n'):
    s = line.strip()
    if re.match(r'^## META BLOCK', s, re.I) or re.match(r'^## Meta (title|description)', s, re.I):
        in_meta_block = True
    if re.match(r'^## PAGE CONTENT', s, re.I):
        in_meta_block = False
    if in_meta_block:
        continue
    if s.startswith('ADD ') or s.startswith('|') or s.startswith('#') or (s.startswith('**') and 'Variant' in s):
        continue
    for m in re.finditer('\u2014', line):
        em_dash_hits.append((line, m.start()))
print(f"[1] EM DASHES: {len(em_dash_hits)}")
for line, pos in em_dash_hits:
    ctx = line[max(0, pos-50):pos+50].replace('\n', ' ')
    print(f"    ...{ctx}...")
    issues.append("Em dash")

# ── 2. POV violations ─────────────────────────────────────────────────────────
pov_hits = list(re.finditer(r'\borganizations\s+(can|need|should|must|are|have|who)\b', content, re.I))
print(f"\n[2] POV VIOLATIONS (organizations + verb): {len(pov_hits)}")
for m in pov_hits:
    ctx = content[max(0, m.start()-30):m.start()+80].replace('\n', ' ')
    print(f"    ...{ctx}...")
    issues.append("POV violation")

# ── 3. Passive voice ──────────────────────────────────────────────────────────
passives = list(re.finditer(r'\b(was|were)\s+\w+ed\s+by\b', content, re.I))
print(f"\n[3] PASSIVE VOICE (was/were Xed by): {len(passives)}")
for m in passives:
    ctx = content[max(0, m.start()-30):m.start()+60].replace('\n', ' ')
    print(f"    ...{ctx}...")
    issues.append("Passive voice")

# ── 4. AI writing patterns ────────────────────────────────────────────────────
ai_patterns = [
    'testament to', 'pivotal', 'seamless', 'groundbreaking', 'evolving landscape',
    'leverage', 'empower', 'synergy', 'serves as a', 'functions as a',
    "in today's", 'in conclusion', 'delve', 'it is important to note',
    "it's important to note", 'boasts', 'revolutionary', 'breathtaking',
]
print("\n[4] AI WRITING PATTERNS:")
found_ai = []
for p in ai_patterns:
    if p.lower() in content.lower():
        found_ai.append(p)
        issues.append(f"AI pattern: {p}")
if found_ai:
    print(f"    FOUND: {found_ai}")
else:
    print("    CLEAN")

# ── 5. Paragraph length (>= 4 sentences) ─────────────────────────────────────
print("\n[5] PARAGRAPHS >= 4 SENTENCES:")
paragraphs = content.split('\n\n')
long_count = 0
in_meta = False
for para in paragraphs:
    stripped = para.strip()
    if not stripped:
        continue
    if re.match(r'^## META BLOCK', stripped, re.I) or re.match(r'^## Meta (title|description)', stripped, re.I):
        in_meta = True
    if re.match(r'^## PAGE CONTENT', stripped, re.I):
        in_meta = False
    if in_meta:
        continue
    if (stripped.startswith('#') or stripped.startswith('|') or
            stripped.startswith('ADD ') or stripped.startswith('[') or
            stripped.startswith('*') or stripped.startswith('-') or
            stripped.startswith('**') or
            re.match(r'^Meta (title|description)', stripped, re.I)):
        continue
    sentences = re.findall(r'[.!?]\s+[A-Z]', stripped)
    count = len(sentences) + 1
    if count >= 4:
        long_count += 1
        issues.append("Paragraph >= 4 sentences")
        print(f"    [{count} sentences] {stripped[:150]}...")
if long_count == 0:
    print("    All paragraphs <= 3 sentences")

# ── 6. Number rule (spell out 1-9 in prose) ──────────────────────────────────
print("\n[6] NUMERAL CHECK (single digits in prose):")
numeral_hits = list(re.finditer(r'(?<![a-zA-Z\d\-\/])([1-9])\s+(?![\d\+\%])', content))
numeral_issues = []
for m in numeral_hits:
    ctx = content[max(0, m.start()-30):m.start()+40].replace('\n', ' ')
    if '|' in ctx or 'SCREENSHOT' in ctx or 'Meta' in ctx:
        continue
    numeral_issues.append(ctx)
for ctx in numeral_issues[:5]:
    print(f"    Check: ...{ctx}...")
if not numeral_issues:
    print("    No obvious violations")

# ── 7. H3 subheadings in body ─────────────────────────────────────────────────
print("\n[7] H3 SUBHEADINGS IN BODY:")
h3_hits = []
in_meta = False
for line in content.split('\n'):
    s = line.strip()
    if re.match(r'^## META BLOCK', s, re.I) or re.match(r'^## Meta (title|description)', s, re.I):
        in_meta = True
    if re.match(r'^## PAGE CONTENT', s, re.I):
        in_meta = False
    if in_meta:
        continue
    if s.startswith('### '):
        h3_hits.append(s)
        issues.append(f"H3 subheading found: {s[:60]}")
if h3_hits:
    for h in h3_hits:
        print(f"    FAIL: {h[:80]}")
else:
    print("    CLEAN")

# ── 8. Custom BANNED: strings from reference/qa_rules.md ──────────────────────
print("\n[8] CUSTOM QA RULES:")
qa_rules_path = Path(__file__).parent.parent / "reference" / "qa_rules.md"
custom_banned = []
if qa_rules_path.exists():
    for line in qa_rules_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("BANNED:"):
            phrase = line[len("BANNED:"):].strip()
            if phrase:
                custom_banned.append(phrase)

if not custom_banned:
    print("    No custom rules defined in reference/qa_rules.md")
else:
    found_custom = []
    for phrase in custom_banned:
        if re.search(re.escape(phrase), content, re.IGNORECASE):
            found_custom.append(phrase)
            issues.append(f"Custom banned phrase: {phrase}")
    if found_custom:
        print(f"    FAIL \u2014 banned phrases found: {found_custom}")
    else:
        print(f"    CLEAN ({len(custom_banned)} rule(s) checked)")

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"TOTAL GENUINE ISSUES: {len(issues)}")
for i in issues:
    print(f"  \u2022 {i}")
