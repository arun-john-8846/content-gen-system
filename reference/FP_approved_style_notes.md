# ADAudit Plus Feature Page — Approved Style Notes

Extracted from two human-reviewed and edited approved pages:
- `account-lockout-tool_edited.docx`
- `windows-file-server-audit_edited.docx`

These are the post-editor versions. All rules below reflect the actual published output, not the pre-edit draft.

Load this file before drafting. Apply all rules below. Where these notes conflict with FP_writer_instructions.md, defer to the approved examples here.

---

## 1. Intro paragraph (below H1)

**Pattern:** 1–3 short sentences. States what the product does + the concrete outcome for the user. No scene-setting. No feature lists. Sentence count varies by topic — simpler topics carry one sentence cleanly; complex topics may use two or three short sentences.

**Approved examples:**

Account lockout (3 sentences):
> ADAudit Plus identifies the source of every Active Directory account lockout. It shows the machine, IP address, process, and root cause. Your team stops guessing and starts fixing.

Windows file server (1 sentence):
> ADAudit Plus gives you visibility into file access, modification, deletion, and permission change actions across your Windows file servers, so you always know who did what, when they did it, and from which machine.

**Do NOT write intros like:** "You get 300+ pre-configured reports, a built-in User Behavior Analytics engine, automated incident response, and..." — this is a feature dump, not an outcome statement.

---

## 2. Capability grid (top of page, above H2 sections)

**Drafting process:** Draft 8 candidate cards (4×2) per `FP_writer_instructions.md`. User selects final set for published page.

**Published output format:** 2-column table. Row count varies by topic — account lockout published = 3 rows (6 cards); file server published = 2 rows (4 cards). No fixed row count. No "Card" number column.

**Cell structure:**
```
**Heading text**
Body text (25–35 words, one sentence preferred).
```

**Example cell:**
> **Identify the lockout source**
> The Account Lockout Analyzer traces every lockout to its origin — the specific device, service, mapped drive, or browser session submitting bad credentials — without manual log correlation.

**Rules:**
- Heading bolded inside the cell — not a separate column
- Body is outcome-focused, not feature-descriptive
- 2 cards per row (2 columns), 4 rows minimum

---

## 3. Screenshot placeholder format

**Format:** Single-column table with 3 rows (not inline text):

| Row | Content |
|---|---|
| 1 | `ADD SCREENSHOT HERE — [Report Name]` |
| 2 | `Navigation: [Full navigation path]` |
| 3 | `Alt text: [Full descriptive alt text]` |

**Example:**
```
ADD SCREENSHOT HERE — Account Lockout Analyzer
Navigation: Active Directory > AD Changes > User Management > Recently Locked Out Users
Alt text: Recently Locked Out Users report showing locked account name, lockout source machine, caller IP address, locking process or device identified by the Account Lockout Analyzer, and logon history leading up to the lockout
```

---

## 4. Body section bullet lists

**Format:** Plain declarative bullets. No **Bold label:** lead-in pattern.

**Approved:**
> - Stale credentials stored on a device after a password change
> - Mapped drives authenticating with an old password
> - Mobile devices using cached credentials that were not updated

**Do NOT write:**
> - **Stale credentials:** Devices that were not updated after a password change...

---

## 5. Benefits grid (bottom of page, before CTA)

**Drafting process:** Always draft 8 cards (2×4). User selects the final set for the published page.

**Published output format:** 2-column table. Row count reflects the cards the user selected.

**Cell structure:** `**Outcome-framed heading**\nBody sentence.`

**Rules:**
- Always draft 8 cards — never fewer
- Headings are outcome-framed ("Resolve in minutes, not hours") as the default; feature-count headings ("300+ pre-configured reports", "14 file storage platforms covered") are acceptable only when the count itself communicates the outcome
- Body expands on the outcome — does not repeat what capability cards already said

**Approved examples (account lockout — outcome-framed):**
> **Resolve in minutes, not hours**
> The lockout source, the originating machine, and the preceding logon history are all in the same report row — no pivoting between tools, no manual DC correlation.

> **Catch attacks before they escalate**
> UBA baselines flag lockout volume spikes and off-hours activity the moment they exceed normal. A brute-force pattern surfaces before it starts affecting users.

**Approved examples (file server — feature-count framed):**
> **300+ pre-configured reports**
> Every file event type, permission change, compliance framework, and summary view has a dedicated report ready to run. No query writing or scripting required.

> **14 file storage platforms covered**
> NetApp, EMC Isilon, Synology, Hitachi NAS, Amazon FSx, Azure File Share, Nutanix Files, QNAP, and more, audited from the same console alongside Windows File Server.

---

## 6. "Why teams choose" heading

After the benefits grid and before the bottom CTA, include a transition heading. Two approved forms:

**Full form (preferred):**
> Why teams choose ADAudit Plus for [topic]

**Short form (acceptable):**
> Why ADAudit Plus

**No body copy under it.** The benefits grid above it serves as the body. This heading acts as a label and transition to the CTA.

---

## 7. Bottom CTA

Two buttons, centred:
```
[ Download free trial ]  [ Schedule a personalized demo ]
```

Note: "personalized" (not "personalised") — US English.

---

## 8. FAQ answer length

Answer length depends on question type:

**Factual / specific questions** ("What causes lockouts?" "Does ADAudit Plus alert in real time?") — **max 2 sentences, no paragraph breaks.**

> The most common causes are stale credentials on a device after a password change, mapped network drives authenticating with an old password, mobile devices using cached credentials, and scheduled tasks or services running with an outdated password. The Account Lockout Analyzer identifies exactly which one triggered the event.

**Conceptual / process questions** ("What is file server auditing?" "Why audit your file server?" "How do I audit Windows file server changes?") — may use a short paragraph plus bullets if the question genuinely requires structured explanation. Keep it tight — no padding.

> File server auditing is the continuous monitoring and recording of every operation that affects files, folders, and permissions on your file servers. A complete audit trail captures who performed each action, what changed, when it happened, and from which machine. Without it, you cannot reliably detect unauthorized access, investigate a security incident, or demonstrate to an auditor that access controls are working.

---

## 9. Internal links record in publish doc

At the end of the publish doc, include a section titled:

`INTERNAL LINKS APPLIED (remove before publishing)`

List every link applied with:
- Anchor text
- Destination URL (slug only or full)
- Section where the link appears

**Format:**
```
1. 'anchor text' — destination-page.html — Section name where it appears
```

---

## 10. "Why native tools fall short" section structure

Both approved pages use bullet lists inside this section rather than prose-only paragraphs.

**Pattern:**
1. One or two short paragraphs explaining the native tool limitations
2. A "Neither tool handles:" or "[Native tool] does not handle:" bullet list
3. Closing paragraph positioning ADAudit Plus

**Approved example (account lockout):**
> Microsoft provides two free utilities for investigating account lockouts, and both have real limits that matter at scale.
>
> LockoutStatus.exe: queries every contactable domain controller... It does not tell you what caused it.
> ALTools.exe (ALockout.dll): designed for client-side investigation... Microsoft explicitly warns against running it on servers...
>
> Neither tool handles:
> - Real-time alerting when a lockout occurs
> - Historical trend analysis or lockout frequency baselines
> - UBA-driven anomaly detection for lockout spikes
> ...

---

## 11. Capability table (What ADAudit Plus audits)

**Format:** 2-column table with shaded header row.

| Header col 1 | Header col 2 |
|---|---|
| Area name | What ADAudit Plus captures (full sentence) |

Each row body is a complete sentence, not a bullet list inside the cell.

---

## 12. Internal link placement for compliance standards

When naming compliance standards (SOX, HIPAA, PCI-DSS etc.) in the compliance section, link the standard name directly to its dedicated compliance report page, not to the generic compliance hub.

**Approved (file server page):**
- 'HIPAA' → hipaa-compliance-reporting-tool.html
- 'PCI-DSS' → pci-dss-compliance-reports.html
- 'SOX' → sox-compliance-auditing-reporting.html

---

## 13. Report name + colon pattern in capability sections

When listing multiple named reports within a capability section, use the `Report Name: description` inline pattern. The report name is the subject; the colon introduces what it does for the IT admin.

**Approved examples:**
> Recently Locked Out Users: gives you every lockout event across all domain controllers in a single view, so you can spot recurring patterns, repeat accounts, and distributed spikes.

> Unusual Volume of Lockout: fires when lockout frequency exceeds the learned domain baseline.

This pattern is distinct from the banned **Bold label:** format — report names are Type A terms and are permitted as subjects. Do not bold them in this inline list context.

---

## 14. Naming specific tools in "Why native tools fall short"

Naming specific Microsoft utilities (LockoutStatus.exe, ALTools.exe, Event Viewer, PowerShell) is permitted in this section. Keep claims high-level — list what the tools cannot do, not technical version-specific internals.

**Approved pattern (account lockout):**
> Microsoft provides two free utilities (LockoutStatus.exe and ALTools.exe) for investigating account lockouts, and both have real limits. Neither tool handles: [bullet list of gaps]

**Approved pattern (file server):**
> Windows provides file event logging through the Security event log and Event Viewer, but both have significant gaps for continuous file server auditing.
> [Then: Event Viewer bullet list, PowerShell bullet list]

---

## What the approved pages do NOT have

- No "| Card | Heading | Body |" three-column grid tables
- No feature-list intro sentences
- No bold lead-in labels in bullet lists (report name + colon pattern is permitted — see #13)
