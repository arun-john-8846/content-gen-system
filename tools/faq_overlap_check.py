#!/usr/bin/env python3
"""Check if FAQ questions overlap with body H2 topics."""
import os, re

pages_dir = "output"
slugs = sorted([
    d for d in os.listdir(pages_dir)
    if os.path.isdir(os.path.join(pages_dir, d))
    and os.path.exists(os.path.join(pages_dir, d, f"{d}_publish.md"))
])

STOPS = {
    'the','a','an','in','on','of','for','to','with','how','what','does','do',
    'is','are','can','you','your','i','it','my','has','have','will','and','or',
    'that','this','which','when','where','why','who','all','at','by','from',
    'as','be','been','not','we','they','their','there','was','were','use',
    'adaudit','plus','active','directory','windows'
}

BOILERPLATE = {'compelling','reasons','choose','capability','capabilities','overview'}


def keywords(text):
    words = re.sub(r'[^a-z0-9\s]', ' ', text.lower()).split()
    return {w for w in words if len(w) > 3 and w not in STOPS}


overlaps = {}

for slug in slugs:
    path = os.path.join(pages_dir, slug, f"{slug}_publish.md")
    with open(path) as f:
        content = f.read()

    faq_m = re.search(
        r'^## (?:FAQ|Frequently asked questions)\s*$',
        content, re.MULTILINE | re.IGNORECASE
    )
    if not faq_m:
        continue

    body = content[:faq_m.start()]
    faq_section = content[faq_m.start():]

    body_h2s = [
        h for h in re.findall(r'^## (.+)$', body, re.MULTILINE)
        if not any(b in h.lower() for b in BOILERPLATE)
    ]

    faq_qs = (
        re.findall(r'^\*\*(.+\?)\*\*\s*$', faq_section, re.MULTILINE)
        or re.findall(r'^### (.+)$', faq_section, re.MULTILINE)
    )

    hits = []
    for fq in faq_qs:
        fq_kw = keywords(fq)
        for h2 in body_h2s:
            shared = fq_kw & keywords(h2)
            if len(shared) >= 2:
                hits.append((fq[:75], h2[:75], sorted(shared)))

    if hits:
        overlaps[slug] = hits

print(f"Pages with potential FAQ/body overlap: {len(overlaps)}/{len(slugs)}\n")
for slug, items in overlaps.items():
    print(f"\n{'='*65}")
    print(f"  {slug}")
    for fq, h2, shared in items:
        print(f"  FAQ: {fq}")
        print(f"   H2: {h2}")
        print(f"  Shared: {shared}")

if not overlaps:
    print("PASS: No FAQ questions overlap with body H2 topics.")
