# Resumes — Multi-Resume System

Several resumes for **Germán Küber**, one per technology focus (Blockchain, Rust, .NET,
Backend, AI, Python, Full Stack, CTO, Engineering Manager) — maintained without the
chaos of editing N PDFs by hand every time something changes.

## How it works

Each resume is a **self-contained HTML file** with its CSS embedded, rendered to PDF
with [WeasyPrint](https://weasyprint.org/). There is no shared template and no build
merge step — every resume is fully independent, so each can diverge in style and
framing without coupling. All resumes keep an **identical structure** (same section
names, same CSS classes) so cross-resume edits stay predictable.

See [`CLAUDE.md`](./CLAUDE.md) for the full architecture, formatting decisions, the
page-break guardrail, and the honesty rules.

## Repo layout

One folder per resume — the folder name is the technology angle. Inside each, the HTML
and PDF are both named `Germán Küber`:

```
AI/                 Germán Küber.html  ·  Germán Küber.pdf
Backend/            Germán Küber.html  ·  Germán Küber.pdf
Blockchain/         Germán Küber.html  ·  Germán Küber.pdf
CTO/                Germán Küber.html  ·  Germán Küber.pdf
Engineering Manager/ Germán Küber.html ·  Germán Küber.pdf
Full stack/         Germán Küber.html  ·  Germán Küber.pdf
Python/             Germán Küber.html  ·  Germán Küber.pdf
Rust/               Germán Küber.html  ·  Germán Küber.pdf
dotnet Architect/   Germán Küber.html  ·  Germán Küber.pdf
```

## Skills (slash commands)

This repo ships three Claude Code skills under `.claude/skills/`. They appear as slash
commands when Claude Code is started in this directory.

### `/update-resume <change>`

Apply a content change to one, several, or all resumes. The skill asks which resumes to
target, plans the work, edits the selected HTML files (adapting wording per resume),
regenerates the PDFs, validates each one visually, and reports back.

```
/update-resume add Node.js to the skills section
/update-resume change the Borderless job title to Lead
```

### `/ats <job description>`

Quick ATS-style keyword match. Paste a job posting; the skill extracts and categorizes
its keywords, runs the fixed `ats_score.py` scorer, and prints a colored comparative
table ranked by match % — which resume fits the posting best.

```
/ats <paste the full job posting here>
```

### `/ats-deep <job description>`

Detailed ATS analysis. Same scorer as `/ats`, but with the full breakdown: per-resume
matched and missing keywords, knockout (qualification) pass/fail gating, synonym-only
matches, and honest suggestions for the best-fit resume.

```
/ats-deep <paste the full job posting here>
```

> The ATS skills **simulate a third-party resume scanner** (Jobscan-style) — there is
> no universal "ATS score." They measure the keyword match and surface gaps honestly;
> they never invent or recommend false keywords.

## Generating a PDF manually

```sh
weasyprint "Blockchain/Germán Küber.html" "Blockchain/Germán Küber.pdf"
```

Install dependencies once:

```sh
pip install weasyprint pypdf pdf2image
```

Some OSes need system libraries (pango, cairo). On macOS with Homebrew the libs live in
`/opt/homebrew/lib`; if WeasyPrint cannot find them, prefix the command with
`DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`.

## Validating a change

Editing the HTML is not enough — it does not reveal how the page renders. After any
layout-affecting change:

1. Regenerate the PDF.
2. Count the pages — 2 is preferred, but going longer is fine if the content justifies
   it; what matters is no tiny orphaned fragment alone on the last page.
3. Render to images and review visually.

The `/update-resume` skill does all of this automatically.
