# Project context: Multi-resume system (Germán Küber)

## Goal
Maintain several resumes, each oriented to a different technology (Blockchain, Rust,
.NET, Backend, AI, Python, Full Stack, CTO), without the chaos of editing N PDFs by
hand every time something changes.

Two kinds of content exist:
- **Cross-resume / generic**: appears in every resume (contact info, education,
  community, languages, most of the work history, achievements). Example: "add
  Node.js everywhere".
- **Technology-specific**: changes per resume (headline, skill order and emphasis,
  which bullets are surfaced at the top, which keywords are prioritized).

## Architecture (decided)
**Camino A — one self-contained HTML file per resume.**

- Each resume is a standalone HTML file with its CSS embedded in `<style>`.
- No `shared.json`, no single template, no build merge step.
- A cross-resume change is applied **manually in each HTML file**, adjusting how it
  fits that specific resume's framing. This is intentional: full control, nothing
  breaks "at a distance".
- All resume HTML files should keep an **identical structure** (same section names,
  same shape of experience blocks, same CSS classes). Use `Blockchain/Resume.html`
  as the reference template and normalize the others to it. Identical structure
  makes cross-resume edits predictable.

`shared.json` was explicitly rejected by Germán: he prefers repeated content per
file so each resume can diverge in style/framing without coupling.

## Technical pipeline (validated, works)
Pipeline: **HTML + CSS → PDF with WeasyPrint**.

1. Each resume is a standalone HTML file with embedded CSS.
2. Generate the PDF: `weasyprint resume.html resume.pdf`
3. Install: `pip install weasyprint` (this environment needed `--break-system-packages`;
   a normal local env does not). Some OSes need system libs (pango, cairo) —
   on Ubuntu: `apt-get install libpango-1.0-0 libpangocairo-1.0-0`.

WeasyPrint was chosen over reportlab because the design lives in CSS (separate from
content), which is what makes it reusable across resumes.

## CRITICAL VALIDATION RULE (do not skip)
**Editing the HTML is not enough.** The HTML does not reveal how it renders: where a
line breaks, whether a bullet wraps badly, whether content overflows onto an extra
page. That is only visible by rendering.

After ANY change that affects layout, ALWAYS:
1. Regenerate the PDF.
2. Count the pages: `python3 -c "from pypdf import PdfReader; print(len(PdfReader('resume.pdf').pages))"`
   — 2 pages is preferred, but not a hard limit. Going over 2 pages is fine if the
   content justifies it. What matters is that the last page does not end with a tiny
   orphaned fragment (e.g. a single line or heading alone on a page).
3. Render to images and review visually:
   ```python
   from pdf2image import convert_from_path
   for i, im in enumerate(convert_from_path('resume.pdf', dpi=90)):
       im.save(f'page_{i+1}.png')
   ```
   (requires `poppler-utils`). Confirm no line/bullet is broken and nothing overflows.
4. For multi-resume changes: a generic change (e.g. a longer bullet) can overflow in
   one resume and not another. Validate EACH PDF visually — do not assume that if one
   is fine the rest are.

If it overflows, the fine-tuning adjustments that worked: lower `font-size` (8.6pt
body), `line-height` (~1.22), page margins (`@page margin: 1cm 1.3cm`), and `margin-top`
on `<h2>`. Fine trims, not a redesign.

## Page-break guardrail (required)
The CSS in every resume must enforce three rules to prevent orphaned headings and
split sections:

1. **Experience roles** — each role wrapped in `<div class="role">` and the CSS
   includes `.role { break-inside: avoid; }`. Without this the paginator can split a
   role across pages — title/meta orphaned at the bottom of one page, bullets
   starting on the next. The wrapper keeps title + meta + bullets together; if a
   role does not fit, the whole role moves to the next page.
2. **Section headings** — `h2 { break-after: avoid; }`. Without this an `<h2>`
   (Education, Key Achievements, Open Source, Spoken Languages, etc.) can stay at
   the bottom of one page while its content starts on the next — or worse, a few
   items appear on one page and the rest on the next. `break-after: avoid` pulls the
   heading down with its first item.
3. **Short compact lines** — `.edu-line, .ach-line, .expertise-line { break-inside: avoid; }`.
   These are the single-line items in Education, Key Achievements, Open Source and
   Core Expertise. Keeping them atomic prevents a line from splitting mid-wrap if it
   lands on a page boundary.

All three are mandatory and live in the `<style>` block of every resume HTML in this
repo. If you add a new section with its own short-line class, give it
`break-inside: avoid` too.

## Resume formatting (decided)
- Single column, no tables, no charts, no multi-column → ATS-friendly (Greenhouse and
  others). Tables/columns break parsing.
- 2 pages preferred, but not a hard limit — a resume may go longer if the content
  justifies it. Do not cut real content just to hit 2 pages.
- Sans-serif font (Helvetica/Arial), headers in blue `#2a4d7a` with a bottom border.
- Justified text in bullets and paragraphs.

## Honesty rules (always respect)
- Do not invent skills, certifications, or experience.
- Distinguish "does not have X" vs "the resume does not show X".
- Do not exaggerate numbers (team size, P&L, etc.).
- If a change makes a strong claim (e.g. "led 200 people"), the wording must match
  the exact reality so it holds up in an interview.

## Specific content already decided (reference)
Worked and validated for the Blockchain resume → useful reference for the others:

- **Blockchain headline**: "Senior Blockchain Engineer — Rust, Node.js / TypeScript,
  MEV & Multi-Chain Infrastructure". (Blockchain identity, but Node/TS visible at top.)
- **Node.js / TypeScript**: must appear in EVERY resume now. Used in production at
  Borderless, Rocking, KliverAI, ClaudeX and CloudX. Listed as a featured language and
  in experience bullets.
- **Web3 tooling**: ethers.js, viem, web3.js, @solana/web3.js — all four confirmed.
- **DeFi protocols**: AMMs = Uniswap V2/V3, Curve, Raydium, PumpSwap. NOTE: **Aave is
  lending, NOT an AMM** — keep that distinction (interview pitfall to avoid).
- **Paramo Technology**: had **company-wide architecture authority** — part of and
  accountable for every cross-team technical decision across 9+ teams (200+
  professionals, each with its own coordinator), working directly with the CTO. This
  was NOT line management of 200 people — it is cross-cutting technical leadership.
  Keep that framing (honest and defensible).
- **CloudX**: was a software consultancy (multi-client), Node/TS and .NET depending
  on the client.

## Repo layout
One folder per resume, each containing the HTML and its generated PDF.
The technology of each resume is identified by its folder name:
- `Blockchain/`, `AI/`, `Backend/`, `CTO/`, `dotnet Architect/`, `Full stack/`,
  `Python/`, `Rust/`

## File naming convention (required)
Inside every folder there is **one HTML** and **two PDFs**, all generated from the
same source:

- `Germán Küber.html` — the single source of truth for this resume.
- `Germán Küber.pdf` — canonical short name, kept stable for backward compatibility
  with other skills and tooling.
- `Germán Küber <Folder>.pdf` — recruiter-friendly copy where `<Folder>` is the
  literal folder name (no transformation, no shortening). Same content as the
  canonical PDF — only the filename differs. Examples:
  - `Blockchain/` → `Germán Küber Blockchain.pdf`
  - `AI/` → `Germán Küber AI.pdf`
  - `dotnet Architect/` → `Germán Küber dotnet Architect.pdf`
  - `Engineering Manager/` → `Germán Küber Engineering Manager.pdf`

Both PDFs must always be regenerated together (they share the HTML — they only
diverge in filename). The folder name is what distinguishes one resume from
another at the directory level; the long-name PDF surfaces that distinction in the
file itself, which is what a recruiter sees when downloaded.
