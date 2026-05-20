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
   keeping the underlying facts identical across all resumes.
3. Preserve the structure and the page-break guardrail: experience roles stay wrapped
   in `<div class="role">` and `.role { break-inside: avoid; }` stays in the CSS.

Edit only the resumes in the target set. Never touch a resume the user did not select.

## Step 5 — Regenerate the PDFs

For every resume you edited, regenerate its PDF with WeasyPrint. In this environment
WeasyPrint needs the Homebrew library path:

```
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 -m weasyprint "<folder>/Germán Küber.html" "<folder>/Germán Küber.pdf"
```

Then count the pages of each regenerated PDF:

```
python3 -c "from pypdf import PdfReader; print(len(PdfReader('<folder>/Germán Küber.pdf').pages))"
```

2 pages is preferred but not a hard limit (per CLAUDE.md) — going longer is fine if the
content justifies it.

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
- Page count of each updated resume.
- Confirmation that each PDF was visually validated.
- Anything that needed a fine layout adjustment.
- Any honesty/consistency concern you noticed.

Do NOT commit. Leave the changes staged for the user to review. If they want a commit,
they will ask.
