# Writer instructions

> **PLACEHOLDER — replace with your actual content writing workflow.**
>
> The pipeline loads this file as the primary writing guide for all steps.
> Be specific. The more concrete your instructions, the better the output.

---

## Step 1: Content brief

The brief defines scope before the draft begins. It should include:

- Seed keyword and intent (informational / transactional / navigational)
- Target audience and their pain points
- 3–5 key topics the page must cover
- Competitor angle — what gaps exist in current SERP results
- Recommended H2 headings (4–6)
- Product sections to include
- Internal linking targets
- FAQ questions (5–6 from live PAA results)

## Step 2: Draft

Write the full feature page body following these rules:

- **Word count:** 1,500–1,800 body words (excluding meta block, FAQ, and CTAs)
- **Voice:** Second person (you/your) throughout
- **Structure:** Intro paragraph → capability sections (H2) → FAQ
- **Each H2 section:** 2–3 sentence passage + 2–4 bullet points
- **No H3 subheadings** under body H2s
- **No benefits grid** anywhere in the body
- **Paragraphs:** Maximum 3 sentences each
- **Active voice** as default — rewrite passive constructions
- **No rhetorical openers** — every section opens with a direct declarative statement

## Step 3: Humanize

Remove AI writing patterns. Protect product-specific terminology.
See `humanizer_guide.md` for full humanization rules.

## Step 4: QA

Run qa_check.py against the draft. Fix all flagged issues before delivery.

## Step 5: Deliver

Generate publish file (with meta variants + internal links) and review file (QA scorecard).

---

## Page structure template

```
[Intro paragraph — 2–3 sentences, no product pitch]

## [Topic-direct heading]

[2–3 sentence passage]

- Bullet 1
- Bullet 2
- Bullet 3

## [Second topic heading]

[2–3 sentence passage]

- Bullet 1
- Bullet 2

[...continue for all H2 sections...]

[Bottom CTA]

## FAQ

**[Question from PAA]**
[40–50 word answer]

[...5–6 FAQ items total...]
```
