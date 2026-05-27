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

There are two kinds of resume in this repo. **Only the ATS folders are selectable
targets in Step 2.** The Human resume is handled separately in Step 6.5.

### ATS folders (selectable in Step 2)

One folder per technology angle, each containing `Germán Küber.html` and two
PDFs (canonical + long-name — see CLAUDE.md). Folder names:

- `AI/`
- `Backend/`
- `Blockchain/`
- `CTO/`
- `Engineering Manager/`
- `dotnet Architect/`
- `Full stack/`
- `Python/`
- `Rust/`

Always derive this list by reading the actual directories at runtime (a folder may
be added or removed). Do not hardcode it from memory — list the directories in the
repo root, excluding `.git`, `.claude`, `Human`, and dotfiles.

### Human resume (handled in Step 6.5 — NOT selectable in Step 2)

- `Human/resume.html` — the branded "for humans" resume (with photo, Performance
  Arts, public speaking). Uses Node + Puppeteer instead of Python + WeasyPrint.
- Read `Human/CLAUDE.md` for its specific styling and content rules.
- The skill considers propagating ATS changes to this resume in Step 6.5 *after*
  the ATS edits are complete — it is never a primary target.

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

## Step 6.5 — Propagate to the Human resume (mandatory check, optional execution)

After every ATS resume in the target set has been edited, regenerated, and visually
validated, the change must be considered for propagation to `Human/resume.html` —
the branded "for humans" resume (with photo, Performance Arts, Public Speaking
prominence). Read `Human/CLAUDE.md` if you have not already this session — it
defines what that resume contains and how it differs from the ATS resumes.

### Why this exists

The Human resume and the ATS resumes are two views of the same person. If a recruiter
pulls the ATS PDF and a hiring manager reads the Human one later (or vice versa), they
must not contradict each other. Factual drift between the two surfaces is the failure
mode this step prevents.

### Decision matrix — what to propagate

Before asking the user, classify the change yourself:

| Change type | Default recommendation |
|---|---|
| Factual: corrected date, renamed role, updated metric, fixed title | **Strongly recommend propagating** — inconsistency between the two surfaces is a liability. |
| New skill / language / framework that fits a generalist framing (Cairo, Rust, Anchor, MCP) | **Recommend propagating** — the Human resume is generalist. |
| Hyper tech-specific micro-detail (a Rust-only `tokio` optimization that only made the Rust ATS bullet) | **Recommend skipping** — the Human resume avoids keyword-dense detail. |
| Removed content (deleted a bullet, dropped a role) | **Strongly recommend propagating** if the removed fact was also present in Human/. |
| Pure styling / page-break / typo fix inside ATS HTML | **Skip** — does not apply, the Human uses a different stack. |

### Ask the user (mandatory, even if the recommendation is clear)

Use the AskUserQuestion tool. Phrase the question with your recommendation embedded:

> "I've applied '<change>' to <list of ATS folders>. Based on the type of change
> (<factual / new-skill / tech-specific / removal>), my recommendation is to
> <propagate / skip>. What do you want?"

Options (single-select):

- **Propagate as-is** — same wording, applied to the matching section in `Human/resume.html`.
- **Propagate with tone adjustment** — same fact, rewritten in narrative / less
  keyword-dense style consistent with the rest of the Human resume.
- **Skip Human** — leave `Human/resume.html` untouched.

Default the recommended option to the first slot, with "(Recommended)" in the label.

### If the user chooses to propagate — execute

1. **Read** `Human/resume.html` fully.

2. **Locate the matching section.** The Human HTML uses `<section class="...">`
   blocks with visible `<h2>` headings — find by heading text. Reference mapping:

   | ATS section | Human equivalent |
   |---|---|
   | Skills → Languages list | `<section>` whose `<h2>` is `Skills`, line item beginning with `<strong>...:`Languages:</strong>` |
   | Skills → other category (e.g. AI / LLM Systems, Blockchain & Web3) | Same `<section>`, line item with matching `<strong>` label |
   | A specific experience role (e.g. `<div class="role">KliverAI</div>`) | `<section class="experience">` containing `<h3>KliverAI` or equivalent role title |
   | Key Achievements | `<section>` with `<h2>Key Achievements</h2>` (if present) |
   | Education | `<section>` with `<h2>Education</h2>` |

   If the matching section does not exist in Human/, ask the user (single follow-up
   question) whether to add it or skip. Do not invent placement.

3. **Apply the edit** with the Edit tool. If the user chose "tone adjustment",
   rewrite the wording for the Human resume's style:
   - Less keyword-dense, more narrative.
   - Same underlying facts and numbers — the metric is non-negotiable.
   - Match the existing voice of nearby bullets in Human/resume.html.
   - **Outcome-first rule (Step 1.5) still applies** to new descriptive content.

4. **Preserve the page-break guardrail.** `Human/resume.html` has explicit
   `page-break-before: always` on the `Skills` and `Volunteer Experience` sections.
   Do not remove or weaken them. If your edit makes one of those sections grow
   significantly, expect to re-validate page-breaks in Step 6.7.

### Step 6.6 — Regenerate the Human PDF

```bash
cd Human/
npm run pdf
```

This invokes Puppeteer (NOT WeasyPrint — the Human resume uses a different stack
from the ATS folders). The script writes `Human/Germán Küber.pdf`.

Confirm the file modification timestamp updated. Count pages:

```bash
python3 -c "from pypdf import PdfReader; print(len(PdfReader('Human/Germán Küber.pdf').pages))"
```

The current target is **5 pages** (page-break before Skills, page-break before
Volunteer Experience). Going longer is fine if the content justifies it; orphaned
single-line pages are not.

### Step 6.7 — Visual validation of the Human PDF (screenshots, MANDATORY)

This step is non-negotiable per the user's instruction: every time the Human resume
is regenerated, capture screenshots of all pages and read them.

```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 -c "
from pdf2image import convert_from_path
for i, im in enumerate(convert_from_path('Human/Germán Küber.pdf', dpi=110)):
    im.save('Human/_p{}.png'.format(i+1))
"
```

Read each `Human/_p*.png` with the Read tool. Confirm explicitly, page by page:

1. **Page 1** — header with photo renders, contact line is intact, summary reads
   cleanly, no overflow into header area.
2. **Skills page** (currently page 4) — the `Skills` `<h2>` heading is at the top
   of the page (not orphaned at the bottom of the previous page); every skill
   category line is visible and not split mid-wrap; Soft Skills and Education
   complete on the same page if they fit, otherwise flow naturally.
3. **Volunteer Experience page** (currently page 5, the final page) — opens with
   `Volunteer Experience` heading; Public Speaking, Organizations, Languages, and
   Performance Arts follow; nothing is cut off at the bottom.
4. **Every page** — no experience-role title orphaned at the bottom; no bullet
   wraps mid-word; no `<h2>` heading sits at the bottom with its content on the
   next page.
5. **The edit itself** — the change you propagated actually appears, in the
   expected section, with correct styling.

If any of these fail, fix the HTML (typically by adjusting the page-break
attribute on a nearby `<section>` or by trimming a too-long bullet), regenerate,
and re-validate.

When all five checks pass, delete `Human/_p*.png`.

## Step 7 — Report

Give the user a concise report:

- Which ATS resumes were updated and the exact change applied to each (note any
  per-resume wording adaptation).
- For each new content addition: whether it went in **outcome-style** (and which
  metric carried it) or **task-style** (and why — typically because the user opted
  out per Step 1.5). The task-style cases are useful to revisit later.
- Page count of each updated ATS resume.
- Confirmation that each ATS PDF was visually validated.
- **Human resume status (Step 6.5):** whether it was propagated, with which mode
  (as-is / tone-adjusted) or explicitly skipped. If propagated: which section was
  edited, the resulting page count, and confirmation that the screenshot validation
  in Step 6.7 passed.
- Anything that needed a fine layout adjustment (ATS or Human).
- Any honesty/consistency concern you noticed — especially any divergence between
  what the ATS resumes now say and what the Human resume says (which can happen
  if the user chose to skip propagation for a factual change).
- A reminder that if the Human PDF was regenerated and the user wants it live on
  germankuber.com, they should run `/publish-resume` next.

Do NOT commit. Leave the changes staged for the user to review. If they want a commit,
they will ask.
