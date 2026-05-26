---
name: update-resume
description: |
  Apply a content change to one, several, or all of Germán Küber's technology-oriented
  resumes. The user invokes `/update-resume <what they want to change>`. The skill asks
  which resumes to target (presenting the list of resume folders plus an "All" option),
  then plans the work, edits the selected HTML files, regenerates their PDFs, validates
  each one visually, and reports back.

  Use this skill whenever the user runs `/update-resume`, or asks to "update the
  resumes", "add X to my CVs", "change something in the resumes", or similar.
---

# Resume Update Skill

You are a workflow assistant for the multi-resume system in this repository. The user
runs `/update-resume <change description>` — everything after `/update-resume` is
**what** they want to change. Your job is to apply that change consistently and safely.

First, read `CLAUDE.md` at the repo root if you have not already this session — it
defines the architecture, the page-break guardrail, the honesty rules, and the file
naming convention. Everything below assumes that context.

## The resumes

One folder per resume, each containing `Germán Küber.html` and `Germán Küber.pdf`.
The folder name identifies the technology angle:

- `AI/`
- `Backend/`
- `Blockchain/`
- `CTO/`
- `Engineering Manager/`
- `dotnet Architect/`
- `Full stack/`
- `Python/`
- `Rust/`

Always derive this list by reading the actual directories at runtime (a folder may be
added or removed). Do not hardcode it from memory — list the directories in the repo
root, excluding `.git`, `.claude`, and dotfiles.

## Step 1 — Understand the change

Parse what the user wrote after `/update`. If it is ambiguous (you cannot tell what
concrete text would change), ask a brief clarifying question before proceeding. Do not
guess at facts.

Honesty rule (from CLAUDE.md): never invent skills, certifications, experience, or
numbers. If the change asserts a strong factual claim, the wording must match reality
so it holds up in an interview. If the change is a *fact* (a metric, a title, a
credential, a team size), it should generally be consistent across every resume it
appears in — flag any contradiction you would introduce.

## Step 1.5 — Outcome-first rule (MANDATORY for content additions)

These resumes are written in **outcome / achievement style**, not task style. Every
new bullet should answer "what changed in the world?" — a number, a delta, a scale,
a time saved, a population impacted, a system migrated. Compare:

- ❌ Task style: "Built backend services in Python and integrated LLM providers."
- ✅ Outcome style: "Cut combined API and cloud spend by 45% via model selection,
  prompt compression, and semantic caching across three LLM providers."

**When this rule fires.** Apply this rule when the user is **adding** content to an
experience role, a skill list, a bullet, or any descriptive section. Do NOT apply it
to meta-data changes — phone, dates, role titles, typo fixes, deletions, replacing
an existing fact with a corrected one. Use judgment: the rule is about *new
descriptive content*, not about every edit.

**Algorithm — for each new piece of descriptive content the user wants to add:**

1. Does the user's wording already include a result (a number, %, scale, time,
   population, before→after, business impact)? If YES → skip ahead, write it
   outcome-style as given.
2. If NO — pause and ask the user, with the AskUserQuestion tool, what metric they
   know. Offer 2–3 concrete framings of *that specific addition*, e.g.:
   - "Do you have a % improvement (latency, cost, errors, throughput)?"
   - "Do you have an absolute number (users impacted, requests/sec, team size,
     time saved)?"
   - "Do you have a before / after comparison (X → Y)?"
   - "Do you have a business outcome (revenue lift, sprint carryover reduced,
     bugs cut, customers retained)?"
   Always include an option "I don't have a number — keep it task-style" so the
   user can opt out per addition.
3. If the user supplies a metric → write it as a real outcome bullet, integrating
   the metric naturally; do not bolt the number on at the end.
4. If the user explicitly chooses "keep it task-style" → write the bullet with the
   strongest possible action verb and concrete tooling, but no fake metric, and
   flag it gently in the report: *"<resume>: added '<text>' as task-style — no
   outcome available."* Never invent a number to satisfy this rule (CLAUDE.md
   honesty rule overrides).

**Do not over-ask.** Group the outcome questions per addition, not per resume — the
same fact is going to multiple resumes with the same metric. One round of questions
covers the whole change.

**Reference for tone calibration.** The May 2026 LinkedIn-aligned rewrite is the
canonical outcome-style example for this repo. Look at any role in
`Backend/Germán Küber.html` (KliverAI 500% / 90ms / 95%, Rocking 70% bugs / 40%
revenue / 45% spend, Borderless 10K+ ops/day, 20x TPS, $50M+ flow, $100K+ P&L,
sub-10ms) to see the expected density and shape of an outcome bullet.

## Step 2 — Ask which resumes to target

Use the AskUserQuestion tool. Present a single multi-select question:

- One option per resume folder found in Step 1 (label = folder name).
- Plus a final option labelled **"All resumes"**.

Set `multiSelect: true` so the user can pick one, several, or all. If the user picks
"All resumes", the target set is every folder. Otherwise the target set is exactly
what they selected.

Do not proceed until the user has answered.

## Step 3 — Plan and create tasks

Use TaskCreate to lay out the work before editing anything. At minimum:

1. One task per target resume: "Apply '<change>' to <folder>".
2. One task: "Regenerate PDFs for all edited resumes".
3. One task: "Validate each regenerated PDF visually".
4. One task: "Report results to the user".

Mark each task `in_progress` when you start it and `completed` the moment it is done —
do not batch completions.

Think before editing: the same change usually needs *tone adaptation* per resume. A
bullet for the Rust CV is phrased differently than for the CTO CV even when the
underlying fact is identical. Decide per resume how the change fits that resume's
angle, headline, and which section it belongs in.

## Step 4 — Apply the change

For each target resume:

1. Read the `Germán Küber.html` file fully (the Edit tool requires it).
2. Apply the change with the Edit tool, adapting wording to that resume's focus while
   keeping the underlying facts identical across all resumes. **New bullets must be
   outcome-style per Step 1.5** — the metric you collected goes inside the bullet,
   integrated naturally, not appended.
3. Preserve the structure and the page-break guardrail: experience roles stay wrapped
   in `<div class="role">`; section blocks (Key Achievements, Education, Open Source)
   stay wrapped in `<div class="section">`; the CSS keeps `.role`, `.section`,
   `h2 { break-after: avoid }`, and the `break-inside: avoid` on `.edu-line`,
   `.ach-line`, `.expertise-line` (see CLAUDE.md for the full guardrail).

Edit only the resumes in the target set. Never touch a resume the user did not select.

## Step 5 — Regenerate the PDFs (two per resume)

For every resume you edited, generate **two PDFs** in the same folder, both built
from the same `Germán Küber.html`:

1. **`Germán Küber.pdf`** — the canonical short name, kept for backward
   compatibility with other skills and tooling.
2. **`Germán Küber <Folder>.pdf`** — the recruiter-friendly name where `<Folder>`
   is the literal folder name (so the technology angle is visible in the filename).
   Examples: `Germán Küber Blockchain.pdf`, `Germán Küber AI.pdf`,
   `Germán Küber dotnet Architect.pdf`, `Germán Küber Engineering Manager.pdf`.

Both files have identical content — only the filename differs. In this environment
WeasyPrint needs the Homebrew library path:

```
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 -m weasyprint \
  "<folder>/Germán Küber.html" "<folder>/Germán Küber.pdf"

DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 -m weasyprint \
  "<folder>/Germán Küber.html" "<folder>/Germán Küber <folder>.pdf"
```

Count the pages of the canonical PDF (the second one will be identical):

```
python3 -c "from pypdf import PdfReader; print(len(PdfReader('<folder>/Germán Küber.pdf').pages))"
```

2 pages is preferred but not a hard limit (per CLAUDE.md) — going longer is fine if
the content justifies it.

## Step 6 — Validate visually

Editing HTML is not enough — the HTML does not reveal how it renders. For each edited
resume, render the PDF to images and actually look at them:

```
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 -c "
from pdf2image import convert_from_path
for i, im in enumerate(convert_from_path('<folder>/Germán Küber.pdf', dpi=105)):
    im.save('<folder>/_p{}.png'.format(i+1))
"
```

Read the generated `_p*.png` images with the Read tool. Confirm for each one:

- No line or bullet is broken or overflowing.
- No experience-role title is orphaned at the bottom of a page (the guardrail should
  prevent this, but verify).
- The last page does not end with a tiny orphaned fragment.
- The change you made actually appears and reads cleanly.

If something looks wrong, fix the HTML with fine adjustments (per CLAUDE.md: lower
`font-size`, `line-height`, page margins, or `<h2>` `margin-top` — fine trims, not a
redesign), regenerate, and re-validate.

When validation passes, delete the temporary `_p*.png` images.

## Step 7 — Report

Give the user a concise report:

- Which resumes were updated and the exact change applied to each (note any per-resume
  wording adaptation).
- For each new content addition: whether it went in **outcome-style** (and which
  metric carried it) or **task-style** (and why — typically because the user opted
  out per Step 1.5). The task-style cases are useful to revisit later.
- Page count of each updated resume.
- Confirmation that each PDF was visually validated.
- Anything that needed a fine layout adjustment.
- Any honesty/consistency concern you noticed.

Do NOT commit. Leave the changes staged for the user to review. If they want a commit,
they will ask.
