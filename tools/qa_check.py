#!/usr/bin/env python3
"""QA checker for ADAudit Plus feature page drafts."""
import re, sys

filepath = sys.argv[1] if len(sys.argv) > 1 else 'output/active-directory-auditing_draft.md'

with open(filepath, 'r') as f:
    content = f.read()

issues = []

# 1. Em dashes in body (exclude table dividers, meta block, screenshot placeholders, headings)
em_dash_hits = []
in_meta_block = False
for line in content.split('\n'):
    s = line.strip()
    # Track META BLOCK boundaries: skip until ## PAGE CONTENT or ## Page content
    if re.match(r'^## META BLOCK', s, re.I) or re.match(r'^## Meta (title|description)', s, re.I):
        in_meta_block = True
    if re.match(r'^## PAGE CONTENT', s, re.I):
        in_meta_block = False
    if in_meta_block:
        continue
    if s.startswith('ADD ') or s.startswith('|') or s.startswith('#') or s.startswith('**') and 'Variant' in s:
        continue
    for m in re.finditer('\u2014', line):
        em_dash_hits.append((line, m.start()))
print(f"[1] EM DASHES: {len(em_dash_hits)}")
for line, pos in em_dash_hits:
    ctx = line[max(0, pos-50):pos+50].replace('\n', ' ')
    print(f"    ...{ctx}...")
    issues.append("Em dash")

# 2. POV violations
pov_hits = list(re.finditer(r'\borganizations\s+(can|need|should|must|are|have|who)\b', content, re.I))
print(f"\n[2] POV VIOLATIONS (organizations + verb): {len(pov_hits)}")
for m in pov_hits:
    ctx = content[max(0, m.start()-30):m.start()+80].replace('\n', ' ')
    print(f"    ...{ctx}...")
    issues.append("POV violation")

# 3. ME style
checks = [
    (r'\bon-prem\b(?!ises)', "on-prem used instead of on-premises"),
    (r'\bMS\s+(Windows|AD|Azure|Entra)\b', "MS abbreviation"),
    (r'\bemail\s+(ID|id)\b', "email ID instead of email address"),
    (r'\b200\+\s+report', "200+ reports (should be 300+)"),
    (r'\bADAudit\+\b', "ADAudit+ (should be ADAudit Plus)"),
    (r'\bManageEngine\b', None),  # count check
]
print("\n[3] ME STYLE CHECKS:")
for pattern, label in checks:
    if label:
        hits = re.findall(pattern, content, re.I)
        if hits:
            print(f"    FAIL: {label} — found: {hits[:3]}")
            issues.append(label)
    else:
        print(f"    ManageEngine occurrences: {len(re.findall(pattern, content))}")

print(f"    on-premises occurrences: {len(re.findall(r'on-premises', content))}")
print(f"    300+ occurrences: {content.count('300+')}")

# 4. Passive voice
passives = list(re.finditer(r'\b(was|were)\s+\w+ed\s+by\b', content, re.I))
print(f"\n[4] PASSIVE VOICE (was/were Xed by): {len(passives)}")
for m in passives:
    ctx = content[max(0, m.start()-30):m.start()+60].replace('\n', ' ')
    print(f"    ...{ctx}...")
    issues.append("Passive voice")

# 5. AI writing patterns
ai_patterns = [
    'testament to', 'pivotal', 'seamless', 'groundbreaking', 'evolving landscape',
    'leverage', 'empower', 'synergy', 'serves as a', 'functions as a',
    "in today's", 'in conclusion', 'delve', 'it is important to note',
    "it's important to note", 'boasts', 'revolutionary', 'breathtaking',
]
print("\n[5] AI WRITING PATTERNS:")
found_ai = []
for p in ai_patterns:
    if p.lower() in content.lower():
        found_ai.append(p)
        issues.append(f"AI pattern: {p}")
if found_ai:
    print(f"    FOUND: {found_ai}")
else:
    print("    CLEAN")

# 6. Paragraph length (>= 4 sentences)
print("\n[6] PARAGRAPHS >= 4 SENTENCES:")
paragraphs = content.split('\n\n')
long_count = 0
in_meta = False
for para in paragraphs:
    stripped = para.strip()
    if not stripped:
        continue
    # Track meta block: skip until PAGE CONTENT marker
    if re.match(r'^## META BLOCK', stripped, re.I) or re.match(r'^## Meta (title|description)', stripped, re.I):
        in_meta = True
    if re.match(r'^## PAGE CONTENT', stripped, re.I):
        in_meta = False
    if in_meta:
        continue
    # Skip headings, tables, screenshot blocks, CTAs, bullets, meta block lines
    if stripped.startswith('#') or stripped.startswith('|') or \
       stripped.startswith('ADD ') or stripped.startswith('[') or \
       stripped.startswith('*') or stripped.startswith('-') or \
       stripped.startswith('**') or \
       re.match(r'^Meta (title|description)', stripped, re.I):
        continue
    # Count sentence endings
    sentences = re.findall(r'[.!?]\s+[A-Z]', stripped)
    # Add 1 for the final sentence
    count = len(sentences) + 1
    if count >= 4:
        long_count += 1
        issues.append("Paragraph >= 4 sentences")
        print(f"    [{count} sentences] {stripped[:150]}...")
if long_count == 0:
    print("    All paragraphs <= 3 sentences")

# 7. Number rule (spell out 1-9 in prose)
print("\n[7] NUMERAL CHECK (single digits in prose):")
numeral_hits = list(re.finditer(r'(?<![a-zA-Z\d\-\/])([1-9])\s+(?![\d\+\%])', content))
numeral_issues = []
for m in numeral_hits:
    ctx = content[max(0, m.start()-30):m.start()+40].replace('\n', ' ')
    # Skip if in table, screenshot, or meta block
    if '|' in ctx or 'SCREENSHOT' in ctx or 'Meta' in ctx:
        continue
    numeral_issues.append(ctx)
for ctx in numeral_issues[:5]:
    print(f"    Check: ...{ctx}...")
if not numeral_issues:
    print("    No obvious violations")

# 8. MITRE ATT&CK — must not appear anywhere in output
print("\n[8] MITRE ATT&CK trademark:")
mitre_hits = list(re.finditer(r'MITRE ATT&CK', content))
print(f"    Total 'MITRE ATT&CK' mentions: {len(mitre_hits)}")
if mitre_hits:
    issues.append("MITRE ATT&CK present in output (must be zero)")
    for m in mitre_hits:
        ctx = content[max(0, m.start()-40):m.start()+60].replace('\n', ' ')
        print(f"    FAIL: ...{ctx}...")
else:
    print("    CLEAN (0 mentions)")

# 9. Entra ID rebrand
print("\n[9] ENTRA ID REBRAND:")
first_mention = content.find('Entra ID')
if first_mention >= 0:
    ctx = content[first_mention:first_mention+120]
    if 'previously known as' in content[:first_mention+200]:
        print("    First mention includes 'previously known as' ✓")
    else:
        print(f"    WARNING: First mention may not include rebrand note: ...{ctx}...")
        issues.append("Entra ID rebrand note missing on first mention")

# 10. UBA scope violation
# UBA in ADAP covers: logon, user management, file, process ONLY.
# Out-of-scope: AD object changes, group membership events, OU modifications, GPO changes, permission changes.
print("\n[10] UBA SCOPE VIOLATIONS:")
uba_oos_patterns = [
    (r'(?i)(uba|user behavior|behavioural? baseline)[^\n]*\b(AD object change|object change activity|group membership event|OU modification|GPO change|permission change)\b',
     "UBA baseline references out-of-scope AD change activity"),
    (r'(?i)(uba|anomal|baseline)[^\n]*(group membership change|OU modif|gpo change|permission change)[^\n]*(signal|indicat|detect|flag|surface)',
     "UBA detection claim covers out-of-scope domain"),
]
uba_hits = []
for pat, label in uba_oos_patterns:
    for m in re.finditer(pat, content):
        ctx = content[max(0, m.start()-20):m.start()+120].replace('\n', ' ')
        uba_hits.append((label, ctx))
        issues.append(f"UBA scope violation: {label}")
if uba_hits:
    for label, ctx in uba_hits:
        print(f"    FAIL ({label}): ...{ctx}...")
else:
    print("    CLEAN")

# 11. Competitor names
print("\n[11] COMPETITOR NAMES:")
competitor_pattern = r'\b(PRTG|SolarWinds|Splunk|Varonis|Lepide|Netwrix|Tenable|Quest Software|Semperis)\b'
comp_hits = list(re.finditer(competitor_pattern, content, re.I))
if comp_hits:
    for m in comp_hits:
        ctx = content[max(0, m.start()-30):m.start()+60].replace('\n', ' ')
        print(f"    FAIL — competitor name '{m.group()}': ...{ctx}...")
        issues.append(f"Competitor name: {m.group()}")
else:
    print("    CLEAN")

# 12. No H3 subheadings anywhere in the body
print("\n[12] H3 SUBHEADINGS IN BODY:")
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

# 13. '4 compelling reasons' section present
print("\n[13] 4 COMPELLING REASONS SECTION:")
if re.search(r'##\s+4 compelling reasons to choose ADAudit Plus', content, re.I):
    print("    Present ✓")
else:
    print("    FAIL: section missing")
    issues.append("'4 compelling reasons' section missing")

# Summary
print(f"\n{'='*50}")
print(f"TOTAL GENUINE ISSUES: {len(issues)}")
for i in issues:
    print(f"  • {i}")
