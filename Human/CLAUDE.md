---
type: resume-folder
audience: humans
stack: node-puppeteer
---

# Human/ — the branded resume (with photo, personality content)

This is the "for humans" resume inside the `Resumes/` repo. It lives **next to** the
9 ATS-oriented resume folders (`Blockchain/`, `Rust/`, `Backend/`, etc.) but it is
**not an ATS resume**. It is the version meant for human eyes — LinkedIn, the
"Download PDF" button on `germankuber.com`, a hiring manager who's already
interested.

It used to live in its own repo (`github.com/germankuber/resume`) under
`PersonalSite/GermanKuberResume/`. It was integrated here so a single skill
(`/update-resume`) can keep all resumes consistent. The old repo is archived; the
old local folder was renamed to `PersonalSite/GermanKuberResume.deprecated/`.

## Stack (different from the ATS resumes — read this carefully)

- **Node.js + Puppeteer** (headless Chrome → PDF). NOT WeasyPrint.
- Single source: `resume.html`.
- `scripts/pdf.js` → builds the PDF.
- `scripts/readme.js` → auto-generates the README from `resume.html`.
- `scripts/sync.js` → keeps content / outputs in sync.
- `package.json` defines the npm scripts; `package-lock.json` is committed.

To regenerate the PDF:

```bash
cd Human/
npm install      # only first time
npm run pdf      # writes ./Germán Küber.pdf
```

If you change `resume.html` you MUST regenerate the PDF — `git status` is not enough
because the rendered output is what people actually see.

## What this resume has that the ATS resumes deliberately do NOT

- **Photo** (`germankuber_2.jpg`) as a circular header.
- **Performance Arts** section — stage magic (Círculo Mágico de España), stand-up
  comedy, theater & improv (10+ years), hypnosis & mentalism. Personality content
  that an ATS would punish or a recruiter doesn't want in a tech screen.
- **Public Speaking** prominence — 80+ talks called out with YouTube channel link.
- **Founders / community** focus — Net-Baires (100K+), Crypto Para Mortales,
  Patrones Para Mortales.
- **Web fonts** (Inter + Geist Mono) and **Font Awesome** icons. Both work because
  Puppeteer is real Chrome — WeasyPrint can't render these the same way.

Headline used here: **"Staff Engineer — Systems, AI & Blockchain | Microsoft MVP"**.

## How it differs from the ATS resumes (matrix)

|                | Human/ (this)              | Other folders (ATS)        |
|----------------|----------------------------|----------------------------|
| Audience       | LinkedIn, public web       | ATS systems, recruiters    |
| Photo          | yes                        | no                         |
| Stack          | Node + Puppeteer           | Python + WeasyPrint        |
| HTML count     | 1                          | 1 per folder (9 folders)   |
| Output         | 1 PDF (`Germán Küber.pdf`) | 2 PDFs per folder (canonical + long-name) |
| Multi-column   | OK                         | NEVER (ATS hostile)        |
| Web fonts      | OK                         | NEVER                      |
| Emojis / icons | OK (Font Awesome)          | NEVER                      |
| Personality    | Yes (Performance Arts)     | No                         |

## How `/update-resume` propagates a change to Human/

When the user runs `/update-resume <change>` against one or more ATS folders, the
skill will (after editing the ATS files and validating them) ask whether to also
apply the change here. Three rules:

1. **Factual changes** (a new metric, a corrected date, a renamed role): the skill
   recommends propagating to keep the two versions consistent — a recruiter reading
   the LinkedIn-style PDF and an ATS pulling structured data should not contradict
   each other.
2. **Skill / language additions**: propagate if the addition fits the generalist
   framing of this resume (Cairo, Rust, Anchor — yes). Skip if the addition is a
   hyper-specific micro-optimization that only makes sense in one ATS angle.
3. **Bullets that are very tech-specific to one ATS** (e.g. a Rust-only
   optimization detail in the Rust resume): default to NOT propagating; the
   skill asks before doing it. The Human resume is generalist on purpose.

The skill is responsible for adapting tone — bullets here are written in a more
narrative, less keyword-heavy style than the ATS ones, but the underlying facts are
identical.

## Visual validation (mandatory after every edit)

Same principle as the ATS resumes from `../CLAUDE.md`: editing HTML is not enough.
After `npm run pdf` finishes:

1. Count pages:
   ```bash
   python3 -c "from pypdf import PdfReader; print(len(PdfReader('Germán Küber.pdf').pages))"
   ```
   Current target: 5 pages, with explicit page-breaks before **Skills** and before
   **Volunteer Experience** so neither section gets split mid-page.

2. Render to PNGs and look at them:
   ```bash
   DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 -c "
   from pdf2image import convert_from_path
   for i, im in enumerate(convert_from_path('Germán Küber.pdf', dpi=105)):
       im.save('_p{}.png'.format(i+1))
   "
   ```
   Read each `_p*.png` with the Read tool. Confirm:
   - Skills section starts cleanly on its own page (no orphaned "Languages" row at
     the bottom of the previous page).
   - Volunteer Experience opens the last page along with Public Speaking,
     Organizations, Languages, and Performance Arts.
   - No bullet wraps badly, no role is split between pages, no orphaned heading.

   When validation passes, delete the temporary `_p*.png` images (they are
   gitignored).

## Page-break guardrail in this HTML

`resume.html` already carries explicit `page-break-before: always` on:
- The `Skills` `<section>`
- The `Volunteer Experience` `<section>`

If you add a new section that risks splitting, either wrap it in
`break-inside: avoid` (small section) or `page-break-before: always` (new chapter).

## Where the PDF ends up published

Once regenerated, the PDF can be published to the website by running
`/publish-resume`, which copies `Human/Germán Küber.pdf` →
`../../PersonalSite/personal-site/public/Germán Küber.pdf`, commits and pushes to
the `personal-site` repo. Vercel auto-deploys.

**Never copy by hand.** Use the skill, otherwise the two sides drift apart.

## Honesty rules

Identical to the ATS resumes — see `../CLAUDE.md` "Honesty rules" section. No
invented metrics, skills, or experience. If a strong claim is made it must hold
up in an interview.
