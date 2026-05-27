# Humanization guide

> **PLACEHOLDER — replace with your organisation's AI pattern removal rules.**
>
> The pipeline applies this guide during the humanization step.
> The more specific you are about patterns to remove and terms to protect, the better.

---

## Goal

Remove AI writing patterns that make the content sound machine-generated.
Protect product-specific terminology and technical terms.

---

## AI patterns to remove

### Opener patterns (most visible to readers)

Remove any paragraph or bullet that opens with:
- "In today's [landscape/world/environment]..."
- "It is important to note that..."
- "It's worth noting that..."
- "One of the most important..."
- A gerund phrase (e.g., "Monitoring your environment, you can...")
- "This [noun] allows you to..."

### Sentence-level patterns

- **Over-explanation:** Remove sentences that restate the preceding bullet
- **Hedging:** Replace "can indicate", "may suggest", "could potentially" with declarative statements where technically accurate
- **Bureaucratic setup lines:** Remove "In this section, we will explore..." and equivalents
- **Deliberate short-sentence stacking:** Merge contrast pairs like "X is simple. Y is not." into a single clause

### Word-level patterns (replace with the alternative shown)

| Remove | Use instead |
|---|---|
| leverage | use |
| utilize | use |
| seamlessly | easily, directly |
| robust | comprehensive, full-featured |
| streamline | simplify, reduce |
| empower | let, allow, enable |
| delve into | explore, examine |
| boasts | offers, includes |
| revolutionary | (omit or restate the specific improvement) |
| groundbreaking | (omit or restate the specific improvement) |
| comprehensive solution | (describe what it specifically does) |
| enhance | improve, strengthen |
| testament to | evidence of |

---

## Terms to protect

> **Add your product's terminology here so humanization does not alter them.**

Protected terms fall into categories:

**Type A — Report and alert names (protect exactly as written):**
Add your specific report and alert names here. Example:
- "File Permission Change Report"
- "Logon Failure Alert"

**Type B — Technical terms (do not paraphrase):**
Add product-specific technical terms. Example:
- "Active Directory"
- "Group Policy Object"

**Type C — Brand and product names (exact capitalisation required):**
Add your product and company names.

**Type D — Compliance standard names (exact format required):**
- PCI-DSS, ISO 27001, HIPAA, SOX, GDPR

---

## Two-step self-check

After humanizing, verify:

1. **Pattern check:** Re-read the first sentence of every paragraph. Does any opener pattern remain?
2. **Term check:** Are all Type A/B/C/D terms intact and correctly formatted?
