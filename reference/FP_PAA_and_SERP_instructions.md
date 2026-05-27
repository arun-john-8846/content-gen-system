# Feature Page SERP Research Instructions
# ManageEngine ADAudit Plus — Product Feature Pages

Run every step here before opening a blank document. SERP research is not optional.

---

## Setup — US VPN and Chrome

All research must be conducted from a US IP. Indian IPs return different SERPs — PAA boxes do not appear, and AI Overviews may differ or be absent.

**Required before every session:**
- US VPN active before opening Chrome
- Use Claude in Chrome for all searches
- All Google searches use: `gl=us&hl=en&pws=0`
- Confirm US results: check location indicator at bottom of Google results page, and verify `gl=us` in the tab URL

**If VPN is unavailable:** Do not proceed. Do not substitute Indian SERP results. Pause until US access is confirmed.

---

## Part 1 — AI Overview check

### Why it matters for feature pages

For broad capability keywords ("Active Directory auditing tool," "AD change auditing"), AI Overviews may appear and pull from vendor pages. Understanding what the AI Overview covers helps structure the ME page to either be cited inside it or cover the ground it misses.

### How to check

1. Open Claude in Chrome with US VPN active
2. Search the target keyword with `gl=us&hl=en&pws=0`
3. Check the top of the results page before organic blue links
4. If an AI Overview appears, expand it fully

### What to record

| What to check | What to record |
|---|---|
| Opening answer | What direct answer or product description does it give? |
| Sub-topics covered | List every sub-topic or capability area it mentions |
| Source citations | Which vendor or article pages does it cite? |
| Gaps | What does it omit that an IT admin would still need? |
| Accuracy | Is anything incomplete or inaccurate ME could correct? |

If no AI Overview: record that it was checked and did not appear. Do not skip this step.

### How AI Overview findings change the feature page draft

| Signal | Action |
|---|---|
| Opens with a direct product description | Your H1 intro must also lead directly with what the product does |
| Covers specific capability sub-topics | Your page must cover all of them, plus gaps |
| Cites a competitor page | Read that page first in Part 2 |
| Did not appear | Focus on blue-link organic structure |
| Appeared but gave incomplete or inaccurate information | Own the correction — your page can be the more accurate source |

### Structural rules for AI Overview eligibility (apply during drafting)

- **Answer first, explain second** — the first paragraph must contain a complete standalone answer
- **Keep opening paragraph under 60 words** — tight and scannable
- **H2 headings that mirror how users search** — "How to monitor privileged user activity in Active Directory" performs better than "Privileged account monitoring"
- **Each H2 section must be self-contained** — a reader dropped into any section should understand it without reading what came before
- **Use structured content** — reference tables, short definition paragraphs, and benefit grids are more likely to be cited

---

## Part 2 — Competitor analysis

### Rules

- Read the top ten organic results minimum
- Click actual SERP result links — never guess URLs
- If a page is blocked or paywalled, record as inaccessible and move to the next
- If Chrome disconnects mid-research, stop — record pages read and inform user; do not draft on incomplete research
- If a page returns 404, recover via `site:domain.com keyword` search

### ME's own ranking page

If ME already ranks in the top three for the keyword, read ME's page first (before competitors). Record:
- Sections and sub-topics ME owns that competitors do not cover
- Customer testimonials with specific names or roles
- ME-specific product framings or angles
- Any feature described that is absent from competitor pages

All ME-owned elements must be retained or improved in the new draft.

### For each competitor page, record

Using `get_page_text` in Claude in Chrome (or `document.querySelector('main, article').innerText` as fallback):

- Approximate word count
- All H2 and H3 headings
- Which sections are present:
  - Definition / what is [topic]
  - What to audit / key areas checklist
  - Benefits
  - Core capability descriptions
  - Privileged user monitoring
  - Real-time alerting
  - UBA / threat detection
  - Compliance reporting
  - Hybrid / cloud coverage
  - Native tool limitations
  - FAQ
- Topics covered that other competitors do not (potential gap)
- Topics that are thin, outdated, or inaccurate

### Content gap analysis

**Table-stakes topics (if 7+ competitors cover it, it must be in the draft):**

For AD auditing feature pages, consistently covered topics include: AD change tracking, logon monitoring, GPO auditing, permission changes, account lockout analysis, compliance reporting, and native tool limitations.

**ME's consistently ownable gaps (competitors miss these):**
- Hybrid AD + Entra ID correlated reporting from a single console
- Attack Surface Analyzer with named attack detection (Kerberoasting, Golden Ticket, DCSync, etc.)
- Account Lockout Analyzer with root cause identification (stale creds, mapped drives, mobile devices)
- Custom report profiles (save specific user + action + filter combinations)
- Response automation (alert → auto-create ticket → notify team)
- AdminSDHolder Permission Changes as a named, distinct report
- Inactive/stale account monitoring as a distinct audit area

**Content usefulness test:**
Before including any section, ask: does this help a real IT admin understand, evaluate, or use the product or topic? If yes, include it with depth. If filler or redundant, skip it.

---

## Part 3 — PAA extraction

### Rules

- PAA questions must come from the live US SERP PAA box only — never guessed
- Indian IPs do not show PAA boxes — US VPN must be active
- For product-intent keywords ("active directory auditing tool"), PAA boxes may be absent — this is normal; record that no PAA appeared

### How to extract PAA questions

1. On the same US SERP, locate the People Also Ask box
2. Expand it fully by clicking through available questions to load more
3. Run in the Chrome console:

```javascript
document.querySelectorAll('[data-q]').forEach(el => console.log(el.getAttribute('data-q')))
```

4. Record every question returned
5. If Google Ads overlay obscures the SERP, `get_page_text` on the SERP tab captures the full result list and PAA questions

### How to use PAA on feature pages

Feature pages are not FAQ-first — the primary structure is capability H2 sections. PAA questions are used to:

1. Identify a definitional section if "What is [topic]" appears in PAA — always include this as H2 section 1
2. Surface compliance questions — if "What are the compliance requirements for X" appears, strengthen the compliance section
3. Identify buyer questions — if "Is [product] worth it" or "What is the best [topic] tool" appears, this signals the page needs a benefits section

Do not create a standalone FAQ section on feature pages unless the user explicitly requests one. Weave PAA-derived questions into the relevant H2 sections instead.

---

## Part 4 — Research summary before drafting

You must be able to answer all of the following before opening a blank document. If any answer is missing, return to the relevant part above.

**AI Overview:**
- Did one appear for this keyword? Yes / No
- If yes: What capabilities did it describe? What source did it cite? What did it miss?

**ME's own page:**
- Does ME rank top 3? Yes / No
- If yes: What sections does ME own that competitors miss? (list them — they must be retained)

**Competitor analysis:**
- How many pages were read? (minimum ten)
- What sections do all or most competitors cover? (table-stakes)
- What high-value topics do competitors miss that ME can own?
- Word count range of top competitors?

**PAA:**
- Were PAA questions extracted from the live US SERP?
- If yes: list all questions; which are being addressed in the draft and how?
- If no PAA appeared: record that

**Content plan:**
- Does the draft plan cover all table-stakes sections?
- Does the draft plan include at least one ME-owned angle competitors miss?
- Does the draft plan include content from ME's own ranking page?
- Does the draft plan meet the 1,700–1,800 word target?

Only proceed to drafting once all of the above are confirmed.

---

## Quick reference — Chrome tool patterns

| Situation | Tool and method |
|---|---|
| Reading a competitor page | `get_page_text` on the open tab |
| Cookie consent banner blocks `get_page_text` | `javascript_exec` with `document.querySelector('main, article').innerText` in ~8,000 character chunks |
| Google Ads overlay obscures SERP | `get_page_text` on the SERP tab — captures organic results and PAA in plain text |
| PAA extraction | `javascript_exec` with `document.querySelectorAll('[data-q]').forEach(el => console.log(el.getAttribute('data-q')))` |
| Competitor page returns 404 | `site:domain.com keyword` search — do not guess a second URL |

---

## Entra ID rebrand rule

- **First mention:** "Microsoft Entra ID, previously known as Azure Active Directory (Azure AD)"
- **All subsequent mentions:** "Microsoft Entra ID" only
- **Never:** "Azure AD" alone for any post-July 2023 references
- The rebrand took effect in July 2023