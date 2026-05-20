---
name: ats
description: |
  Simulate an ATS / resume-scanner keyword match between a job posting and Germán
  Küber's resumes. The user invokes `/ats <job description>` — pasting the text of a
  job posting (or a path/URL to it). The skill uses the model's judgment to extract and
  categorize the posting's keywords, then runs the fixed `ats_score.py` script, which
  prints a colored comparative table ranked by match %. The skill just shows that
  table — nothing more. For the detailed breakdown (missing keywords, knockout flags,
  honest suggestions), use `/ats-deep`.

  `/ats` prints exactly one thing — a two-column table of Resume | the keywords that
  did NOT match. For the full breakdown (match %, matched keywords, knockout gating,
  honest suggestions) use `/ats-deep`.

  Use this skill whenever the user runs `/ats`, or asks to "check a job posting against
  my resumes", "which resume fits this job", "ATS match", "keyword match for this
  search", or similar.
---

# ATS Match Skill (`/ats`)

You are a resume-vs-job-posting match analyzer for the multi-resume system in this
repository. The user runs `/ats <job description>` — everything after `/ats` is the
**job posting** to analyze against the resumes.

`/ats` prints exactly one thing: a **two-column table** — Resume | the keywords that
did NOT match — resumes sorted by overall match descending. Nothing else. The deeper
analysis (match %, knockout gating, matched keywords, honest suggestions) lives in the
separate `/ats-deep` skill. Keep `/ats` to exactly what the script prints — do not add
commentary.

## What this skill is — and is NOT

This simulates a **third-party resume scanner** (Jobscan / ResumeWorded style), not any
single real ATS. There is no universal "ATS score" — Greenhouse does not score at all,
Taleo uses exact-string matching, Workday/iCIMS use semantic AI. The table the script
prints already carries the framing line "Scanner-style estimate, not a real ATS score."

## Architecture — strict split

- **The model (you)** extracts and categorizes the posting's keywords and builds the
  synonym list — the parts that need language judgment.
- **The fixed script `ats_score.py`** (in this skill's directory) does all matching,
  scoring and table rendering. It is already written — **never regenerate it**. If its
  behavior must change, edit `ats_score.py` itself and update this doc.

The match % must be reproducible: the same posting always yields the same table. Never
eyeball matches or redo the arithmetic.

## Step 1 — Get the job posting

The user's argument is the job posting — pasted text, a file path, or a URL. If a path,
read it; if a URL, fetch it; if empty or clearly not a posting, ask the user to paste
the posting text.

## Step 2 — Extract and categorize keywords (model judgment)

Read the posting and pull every concrete requirement; ignore filler/boilerplate.
Capture technologies, languages, frameworks, libraries; named tools/products; the job
title and variants; methodologies, certifications, industry terms; explicit
qualifications (degree, minimum years, work authorization, clearance, location); soft
skills the posting explicitly names.

Categorize each: `hard_skill`, `tool`, `title`, `qualification`, `soft_skill`,
`other_keyword`. Record each keyword's frequency in the posting. For each keyword, list
known synonyms / variants to also accept (`JS`↔`JavaScript`, `.NET`↔`dotnet`,
`K8s`↔`Kubernetes`, `Postgres`↔`PostgreSQL`, etc.).

## Step 3 — Build the keywords JSON

Write `/tmp/ats_keywords.json` in the shape `ats_score.py` expects (also documented in
the script header):

```json
{
  "job_title": "Senior Backend Engineer",
  "keywords": [
    {"term": "Rust", "category": "hard_skill", "frequency": 3, "synonyms": []},
    {"term": "Kubernetes", "category": "tool", "frequency": 1, "synonyms": ["K8s"]},
    {"term": "5+ years experience", "category": "qualification", "frequency": 1,
     "synonyms": [], "qualification_kind": "years_experience", "value": 5}
  ]
}
```

`category` ∈ `hard_skill` / `tool` / `title` / `other_keyword` / `soft_skill` /
`qualification`. `qualification` items are ignored by the score — `/ats` does not gate
knockouts (that is `/ats-deep`), but still include them in the JSON so the same file
works for both skills.

Set `job_title` to a short label for the posting (e.g. "Polymarket · Senior Backend
Engineer") — the script prints it as the table heading.

This JSON is the **only** thing you generate. Do not write or regenerate scoring code.

## Step 4 — Run the scorer and show the table

Invoke the fixed script:

```
python3 "<skill_dir>/ats_score.py" /tmp/ats_keywords.json "<repo_root>"
```

`<skill_dir>` is this skill's base directory; `<repo_root>` is the resumes repo root
(the directory holding the resume folders — usually the current working directory).

The script prints a single box-drawn two-column table — `Resume` | `Missing keywords`
(the keywords that did NOT match) — resumes sorted by overall match descending.

**Show that table to the user verbatim, every resume row.** Do not truncate it, do not
add a match %, do not add the matched keywords, do not add prose analysis. The only
thing you may add is one short closing line pointing to `/ats-deep <same posting>` for
the full breakdown (match %, matched keywords, knockout gating, honest suggestions).

Then clean up `/tmp/ats_keywords.json` (the only temp file — `ats_score.py` is a
permanent part of the skill and must NOT be deleted).

Do NOT edit any resume and do NOT commit — this skill is read-only analysis.
