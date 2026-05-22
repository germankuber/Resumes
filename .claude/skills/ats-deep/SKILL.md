---
name: ats-deep
description: |
  Deep ATS analysis of a job posting against Germán Küber's resumes. The user invokes
  `/ats-deep <job description>` — pasting the text of a job posting (or a path/URL).
  Like `/ats` it extracts and categorizes the posting's keywords and runs the fixed
  `ats_score.py` scorer, but it produces the FULL breakdown: per-resume matched and
  missing keywords, knockout (qualification) pass/fail gating, synonym-only matches,
  and honest suggestions for the best-fit resume.

  Use this skill when the user runs `/ats-deep`, or asks for a "detailed ATS analysis",
  "what keywords am I missing", "why does this resume score low", "deep match
  breakdown", or similar. For just the quick comparative table, use `/ats` instead.
---

# ATS Deep Analysis Skill (`/ats-deep`)

You are a resume-vs-job-posting match analyzer for the multi-resume system in this
repository. The user runs `/ats-deep <job description>` — everything after `/ats-deep`
is the **job posting**.

`/ats-deep` is the **detailed** counterpart of `/ats`. `/ats` shows only the
comparative table; `/ats-deep` shows the full breakdown. Both share the same fixed
scorer.

Read `CLAUDE.md` at the repo root first if you have not this session — especially the
honesty rules.

## What this skill is — and is NOT

This simulates a **third-party resume scanner** (Jobscan / ResumeWorded style), not any
single real ATS. There is no universal "ATS score" — Greenhouse does not score,
Taleo uses exact-string matching, Workday/iCIMS use semantic AI. Always frame the
output as a scanner-style estimate.

Critical honesty rule: this skill **measures** the match and shows what is missing. It
must **never** invent or recommend inserting keywords that are not true of Germán's
real experience. Keyword stuffing inflates a score and collapses in the interview.
Surface gaps honestly; the user applies real changes via `/update-resume`.

## Architecture — strict split

- **The model (you)** extracts and categorizes keywords, builds the synonym list,
  judges the knockouts, and writes the honest suggestions — the language-judgment work.
- **The fixed script `ats_score.py`** does all matching and scoring. It lives in the
  **`ats` skill's directory** (`.claude/skills/ats/ats_score.py`) — this skill reuses
  it, it does not have its own copy. **Never regenerate the script.** If its behavior
  must change, edit that one file and update both skill docs.

`ats_score.py` is deterministic for a given keywords JSON, but the keyword extraction
is the model's and varies slightly run-to-run — treat each match % as a ±5-point band
and rely on the resume *ranking* as the stable output. Never eyeball matches or redo
the arithmetic.

## Step 1 — Get the job posting

The user's argument is the job posting — pasted text, a file path, or a URL. If a path,
read it; if a URL, fetch it; if empty or clearly not a posting, ask for the text.

## Step 2 — Extract and categorize keywords (model judgment)

Keyword extraction is governed by the **canonical Step 2 rules in
`.claude/skills/ats/SKILL.md`** — the atomic-keyword definition, the three forbidden
anti-patterns (umbrella / prose / bare-generic), the company-vs-role heuristic, the
weight-3-for-core-stack rule, `frequency` as centrality, synonym handling, and the
mandatory ANTI-OMISSION RULE. Read that section and apply it exactly; do not maintain
a second copy of the rules here.

`/ats-deep` adds nothing to extraction itself — it only reports the result in more
detail. Capture the same keyword set you would for `/ats`, including every
`qualification` item, which Step 5 will gate.

## Step 3 — Build the keywords JSON

Write `/tmp/ats_keywords.json` in the shape `ats_score.py` expects (documented in the
script header):

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

For `qualification` items set `qualification_kind` (`years_experience` / `degree` /
`work_authorization` / `location` / `clearance`) and a `value` where meaningful — you
will need these in Step 5. This JSON is the only thing you generate; do not write
scoring code.

## Step 4 — Run the scorer in JSON mode

Invoke the fixed script with `--json` to get the full machine-readable report:

```
python3 "<ats_skill_dir>/ats_score.py" /tmp/ats_keywords.json "<repo_root>" --json
```

`<ats_skill_dir>` is `.claude/skills/ats/` (the script lives with the `ats` skill, not
this one). `<repo_root>` is the resumes repo root. The `--json` flag makes the script
emit, per resume: `overall`, `subscores`, `matched` (each with an exact/synonym tag),
`missing` — sorted by overall match descending.

If the JSON is large, redirect to a temp file and read it back, or post-process with a
small `python3 -c` one-liner — but never recompute the scores yourself.

## Step 5 — Knockout gating (model judgment)

The script does not judge knockouts. For each `qualification` keyword, decide
PASS / FAIL / UNCLEAR per resume, using the resume content:

- `years_experience` — does the work history support the minimum?
- `degree` — present in Education & Certifications?
- `work_authorization` / `location` — the resumes state "Las Palmas, Spain (EU
  Citizen) — Remote — EU / Americas". Judge against the posting.
- `clearance` — almost certainly absent; flag FAIL/UNCLEAR.

A high keyword % never overrides a failed knockout.

## Step 6 — Full report

Output, in this order:

1. **Framing note** — "Scanner-style estimate, not a real ATS score."

2. **Comparative table** — Resume / Match % / Hard skills / Title / Knockout. You may
   reuse the script's printed table for the first columns; append the Knockout column
   from your Step 5 judgment (PASS / FAIL / UNCLEAR per resume).

3. **Best-fit resume** — name the top resume, then:
   - **Matched keywords**, grouped by category.
   - **Missing keywords**, grouped by category — the concrete gaps.
   - **Knockout flags** with PASS / FAIL / UNCLEAR and a one-line reason each.
   - **Honest suggestions** — for each missing keyword, give ONE of three verdicts:
     1. **Add it** — it is plausibly true of Germán's real experience (his *other*
        resumes already show it) and is a concrete, scannable term. Recommend the
        exact phrasing.
     2. **Do not add** — it would be a false claim; nothing in his history supports
        it. Say so explicitly; a stuffed keyword collapses in the interview.
     3. **Not a scannable skill** — the keyword is an umbrella or prose term
        (e.g. "AI tools", "computer science fundamentals"); it cannot be matched as
        a literal string. Do not chase the phrase itself — cover it with the concrete
        technologies underneath it. If Germán does not have those concrete
        technologies, THAT is the real gap: report it as such, do not paper over it.
     Recommend adding only what is genuinely true; point the user to `/update-resume`
     to apply real changes.

4. **Synonym-only matches** — keywords that matched only via a synonym, per the
   script's tags. An exact-match ATS (e.g. Taleo) would miss these — recommend adding
   the exact phrasing from the posting.

5. **Bottom line** — one short paragraph: which resume to send, the single highest-
   impact honest improvement, and any real limitation of this application.

Clean up `/tmp/ats_keywords.json` when done (`ats_score.py` is permanent — never delete
it). Do NOT edit any resume and do NOT commit — this skill is read-only analysis.
