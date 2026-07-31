# 📄 Resumes — Multi-Resume System

Several resumes for **Germán Küber**, one per technology focus (Blockchain, Rust, .NET,
Backend, AI, Python, Full Stack, CTO, Engineering Manager) — maintained without the
chaos of editing N PDFs by hand every time something changes. ✨

## ⚙️ How it works

Each resume is a **self-contained HTML file** with its CSS embedded, rendered to PDF
with [WeasyPrint](https://weasyprint.org/) 🖨️. There is no shared template and no build
merge step — every resume is fully independent, so each can diverge in style and
framing without coupling. All resumes keep an **identical structure** (same section
names, same CSS classes) so cross-resume edits stay predictable.

📘 See [`CLAUDE.md`](./CLAUDE.md) for the full architecture, formatting decisions, the
page-break guardrail, and the honesty rules.

## 📁 Repo layout

Two kinds of resume live in this repo. They share data but have different audiences,
styling, and rendering stacks.

### 🎯 ATS folders (9 — Python + WeasyPrint, no photo)

One folder per technology angle. Inside each, the HTML and PDFs are named
`Germán Küber`:

```
🤖 AI/                  Germán Küber.html  ·  Germán Küber.pdf
⚙️  Backend/             Germán Küber.html  ·  Germán Küber.pdf
⛓️  Blockchain/          Germán Küber.html  ·  Germán Küber.pdf
🧭 CTO/                 Germán Küber.html  ·  Germán Küber.pdf
👥 Engineering Manager/ Germán Küber.html  ·  Germán Küber.pdf
🎨 Full stack/          Germán Küber.html  ·  Germán Küber.pdf
🐍 Python/              Germán Küber.html  ·  Germán Küber.pdf
🦀 Rust/                Germán Küber.html  ·  Germán Küber.pdf
🟦 dotnet Architect/    Germán Küber.html  ·  Germán Küber.pdf
```

### 🧑 Human resume (Node + Puppeteer, with photo)

```
🧑 Human/   resume.html  ·  Germán Küber.pdf  ·  germankuber_2.jpg
```

The "for humans" resume — LinkedIn, the "Download PDF" button on
[germankuber.com](https://germankuber.com), a hiring manager who's already
interested. Has a photo, a Performance Arts section, Public Speaking prominence,
and uses web fonts + Font Awesome (which is why it needs Puppeteer instead of
WeasyPrint). See [`Human/CLAUDE.md`](./Human/CLAUDE.md) for its content and
styling rules.

## 🛠️ Skills (slash commands)

This repo ships **four** Claude Code skills under `.claude/skills/`. They appear as
slash commands when Claude Code is started in this directory.

> 🔁 **Typical flow:** `/update-resume <change>` (edits ATS folders + asks about
> Human/) → `/publish-resume` (pushes the Human PDF live on germankuber.com).
> `/ats` and `/ats-deep` are read-only diagnostics for matching against a job
> posting.

### ✏️ `/update-resume <change>`

Apply a content change to one, several, or all ATS resumes — and optionally
propagate it to the Human resume. The skill walks 7 steps end-to-end:

1. **Understand the change.** If ambiguous, asks one clarifying question.
2. **Outcome-first check.** If the change adds descriptive content, requires a
   metric (% / number / time / population) before writing it task-style.
3. **Pick the ATS targets.** Multi-select prompt with every ATS folder + an
   "All resumes" option. `Human/` is NEVER a primary target here — it is
   handled separately in step 6.5.
4. **Plan.** Creates one task per target resume plus regenerate/validate/report.
5. **Edit each selected ATS HTML.** Adapts wording per resume's angle while
   keeping the underlying facts identical. Preserves the page-break guardrail
   (roles wrapped in `.role`, sections in `.section`, `h2 { break-after: avoid }`).
6. **Regenerate two PDFs per folder** (`Germán Küber.pdf` + `Germán Küber <Folder>.pdf`)
   with WeasyPrint, then validate visually by rendering each page to PNG and
   reading it.
7. **Propagate to `Human/` (mandatory check, optional execution).** After the
   ATS edits validate, the skill classifies the change (factual / new-skill /
   tech-specific / removal) and asks:
   - **Propagate as-is** — same wording into the matching `<section>` in
     `Human/resume.html`.
   - **Propagate with tone adjustment** — same fact, rewritten narrative-style.
   - **Skip Human** — leave it untouched.

   If you choose to propagate, the skill runs `npm run pdf` inside `Human/` and
   then **screenshots every page of the resulting PDF** and reads each PNG to
   confirm sections are not split, no heading is orphaned, and the change is
   visible. (PNGs are cleaned up after.)
8. **Report.** Per-resume diff summary, page counts, validation results, Human
   propagation status, and a reminder to run `/publish-resume` if you want the
   new Human PDF live on the website.

```
/update-resume add Node.js to the skills section
/update-resume change the Borderless job title to Lead
/update-resume add Polkadot Builder Program to education
```

The skill **does not commit**. Review the working tree yourself afterwards.

### 🚀 `/publish-resume`

Publish the latest `Human/Germán Küber.pdf` to germankuber.com — copies it into
the `personal-site` repo, commits, pushes, and verifies Vercel picked up the
deploy via MCP. Use this whenever you want the "Download PDF" button on the site
to serve the freshly regenerated Human resume.

```
/publish-resume
```

What it does, step by step:

1. **Preconditions.** Checks the Human PDF exists, the `personal-site` repo is
   reachable on `main` with a clean tree, and the source PDF is newer than the
   destination. Stops and asks if anything looks off.
2. **Copy** `Resumes/Human/Germán Küber.pdf` →
   `Personal/PersonalSite/personal-site/public/Germán Küber.pdf`.
3. **Commit and push** in `personal-site` (single file, conventional commit
   message, push to `main`).
4. **Verify Vercel** via the Vercel MCP — finds the `personal-site` project,
   confirms a new deployment was triggered by your push, and reports its
   `readyState` (`BUILDING` → `READY`).
5. **Report** the source/destination PDF sizes, the commit SHA, the deployment
   ID, and the public URL.

What it does NOT do: edit any HTML, regenerate any PDF, touch ATS folders, or
modify site code beyond the PDF asset. Use `/update-resume` first if you need
to change content.

### 🎯 `/ats <job description>`

Quick ATS-style keyword match. Paste a job posting; the skill extracts and
categorizes its keywords, runs the fixed `ats_score.py` scorer, and prints a
colored comparative table ranked by match % — which ATS resume fits the
posting best.

```
/ats <paste the full job posting here>
```

### 🔬 `/ats-deep <job description>`

Detailed ATS analysis. Same scorer as `/ats`, but with the full breakdown:
per-resume matched and missing keywords, knockout (qualification) pass/fail
gating, synonym-only matches, and honest suggestions for the best-fit resume.

```
/ats-deep <paste the full job posting here>
```

> ⚠️ The ATS skills **simulate a third-party resume scanner** (Jobscan-style) —
> there is no universal "ATS score." They measure the keyword match and
> surface gaps honestly; they never invent or recommend false keywords.

## 🖨️ Generating a PDF manually

### ATS folders (WeasyPrint)

```sh
weasyprint "Blockchain/Germán Küber.html" "Blockchain/Germán Küber.pdf"
```

📦 Install dependencies once:

```sh
pip install weasyprint pypdf pdf2image
```

🍎 Some OSes need system libraries (pango, cairo). On macOS with Homebrew the libs
live in `/opt/homebrew/lib`; if WeasyPrint cannot find them, prefix the command
with `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`.

### Human resume (Puppeteer)

```sh
cd Human/
npm install   # first time only
npm run pdf   # writes Human/Germán Küber.pdf
```

The Human resume uses a different stack on purpose — Puppeteer (real Chrome) can
render web fonts, Font Awesome, and decorated section blocks that WeasyPrint
either skips or renders inconsistently.

## ✅ Validating a change

Editing the HTML is not enough — it does not reveal how the page renders. After any
layout-affecting change:

1. 🔄 Regenerate the PDF.
2. 📏 Count the pages — 2 is preferred, but going longer is fine if the content
   justifies it; what matters is no tiny orphaned fragment alone on the last page.
3. 👀 Render to images and review visually.

The `/update-resume` skill does all of this automatically. 🤖
