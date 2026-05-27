---
name: ats
description: |
  Simulate an ATS / resume-scanner keyword match between a job posting and Germán
  Küber's resumes. The user invokes `/ats <job description>` — pasting the text of a
  job posting (or a path/URL to it). The skill uses the model's judgment to extract and
  categorize the posting's keywords, then runs the fixed `ats_score.py` script.

  `/ats` prints two tables: a comparative table (Match % / Hard skills / Title) and a
  missing-keywords table (Resume | the keywords that did NOT match), both sorted by
  overall match. For the full breakdown (matched keywords, knockout gating, honest
  suggestions) use `/ats-deep`.

  Use this skill whenever the user runs `/ats`, or asks to "check a job posting against
  my resumes", "which resume fits this job", "ATS match", "keyword match for this
  search", or similar.
---

# ATS Match Skill (`/ats`)

You are a resume-vs-job-posting match analyzer for the multi-resume system in this
repository. The user runs `/ats <job description>` — everything after `/ats` is the
**job posting** to analyze against the resumes.

`/ats` prints two tables: (1) a comparative table — Resume / Match % / Hard skills /
Title; (2) a missing-keywords table — Resume | the keywords that did NOT match. Both
sorted by overall match descending. The deeper analysis (knockout gating, matched
keywords, synonym callouts, honest suggestions) lives in the separate `/ats-deep`
skill. Keep `/ats` to exactly what the script prints — do not add commentary.

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

`ats_score.py` is fully deterministic: a given keywords JSON always yields the same
table. The keyword extraction, however, is done by the model and can vary slightly
run-to-run, so treat the match % as a ±5-point band, not an exact figure. The stable,
trustworthy output is the *ranking* of resumes. Never eyeball matches or redo the
arithmetic — always run the script.

## Step 1 — Get the job posting

The user's argument is the job posting — pasted text, a file path, or a URL. If a path,
read it; if a URL, fetch it; if empty or clearly not a posting, ask the user to paste
the posting text.

## Step 2 — Extract and categorize keywords (model judgment)

This step decides the quality of the whole analysis. A badly formed keyword shows up
as "missing" in all 9 resumes at once and is noise. Follow these rules exactly.

### 2a — What an atomic keyword is

An **atomic keyword** is a string that satisfies BOTH tests:
- a recruiter would literally type it into a search box, AND
- an engineer would write that exact string in a CV (skills list or a bullet).

If a candidate phrase fails either test, it is not a keyword — reform it or drop it.

### 2b — The three forbidden anti-patterns (with real examples)

Never emit a keyword that is:
1. **An umbrella concept** — a category, not a technology.
   Bad: `AI tools`, `cloud infrastructure`. Nobody writes "AI tools" in a CV.
2. **A descriptive phrase / prose** — a sentence fragment, not a term.
   Bad: `computer science fundamentals`, `real-time pipelines`.
3. **A bare generic term** — too broad to be a skill on its own.
   Bad: `algorithms` (alone). `algorithms` is a CS topic, not a scannable skill.

When you hit one of these, apply 2c (decompose) — do not just emit it.

### 2c — Decompose umbrellas, anchored to the posting

Replace an umbrella with the concrete, atomic terms the posting itself names.
- `cloud infrastructure` → emit `AWS`, `Terraform`, `Kubernetes` ONLY if the posting
  names them. NEVER invent a technology the posting does not mention.
- `AI tools` → emit `LangChain`, `OpenAI API`, `RAG` etc. only if named.
- If the posting names NO concrete members of the umbrella, keep the umbrella as a
  single `other_keyword` with weight 2 and MANDATORY synonyms covering how it is
  actually phrased in CVs — do not promote it to `hard_skill`/`tool`.

### 2d — Company vs. role heuristic

Extract requirements of the ROLE, not descriptions of the company's product.
- Pull keywords from "Responsibilities" / "Requirements" / "What you'll do" sections.
- Ignore "About us" / "Our mission" / product-pitch sections.
- Subject test: if the sentence's subject is the *company* ("we build cybersecurity
  software"), the noun describes the product, not a skill the candidate must have —
  do NOT extract it. If the subject is the *candidate* ("you will build X"), extract.
  Example: `cybersecurity` from a SecurityScorecard posting describes their product,
  not the engineer's required skill — drop it unless the role itself requires it.

### 2e — Weight discipline: reserve weight 3 for the core stack

`hard_skill`/`tool`/`title` carry weight 3. Reserve weight-3 categories for
technologies that are CORE to the role — typically mentioned more than once or
clearly central. Niche / supporting tools (e.g. Jenkins, ArgoCD, New Relic,
ClickHouse) go in `other_keyword` (weight 2), even though they are real tools — this
prevents a niche tool from weighing the same as the core stack (AWS, Node.js).
Do NOT invent a new category or an intermediate weight; use `other_keyword`.

### 2f — `frequency` means centrality, not a literal count

`frequency` is NOT a count of literal appearances. It is the keyword's **centrality
to the role**, on a 1-3 scale:
- 3 = central / defining requirement of the job
- 2 = clearly expected, part of the day-to-day
- 1 = mentioned in passing, nice-to-have
The scorer multiplies weight by `min(frequency, 3)`, so this is the lever that
separates the core stack from the long tail.

### 2g — Synonyms: cover spelling and punctuation variants

For each keyword list known synonyms / variants to also accept: `JS`↔`JavaScript`,
`.NET`↔`dotnet`, `K8s`↔`Kubernetes`, `Postgres`↔`PostgreSQL`. The scorer already
normalizes hyphen/slash/underscore/space variants, so `CI/CD` matches `CI - CD`
automatically — you do NOT need synonyms for pure separator differences. Use synonyms
for genuinely different strings (abbreviations, alternate names, vendor spellings).

### 2h — Do not merge related-but-distinct disciplines

Keep adjacent disciplines as separate keywords. `ML` and `data science` are not the
same skill; `frontend` and `UX` are not the same skill. One keyword per discipline.

### 2i — ANTI-OMISSION RULE (mandatory — read before finishing)

The rules above filter keywords by their FORM (umbrella / prose / company-product),
NEVER by whether they are comfortable or by whether the resumes happen to contain
them. A real gap — a concrete technology the posting requires that Germán does not
have (e.g. `Kubernetes`, `Go`, `Kafka`) — always has the form of a concrete
technology noun, so the form filter is structurally incapable of removing it. If a
keyword is a concrete, scannable technology, it STAYS, even if it will be missing in
all 9 resumes. Dropping a keyword because it is awkward, or because no resume has it,
is keyword stuffing by omission and is forbidden.

### 2j — Self-check before writing the JSON

For every keyword, confirm:
- [ ] An engineer would write this exact string in a CV (2a).
- [ ] It is not an umbrella / prose / bare-generic term (2b) — or it was decomposed.
- [ ] It is a role requirement, not the company's product (2d).
- [ ] weight 3 only for the core stack; niche tools → `other_keyword` (2e).
- [ ] `frequency` reflects centrality 1-3, not a literal count (2f).
- [ ] If it would be missing in all 9 resumes, that is because it is a REAL gap
      (concrete tech noun), not because the keyword is malformed (2i).

Categorize each: `hard_skill`, `tool`, `title`, `qualification`, `soft_skill`,
`other_keyword`.

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

The script prints two box-drawn tables: (1) the comparative table — `Resume` /
`Match %` / `Hard skills` / `Title`, colored by threshold; (2) the missing-keywords
table — `Resume` | `Missing keywords` (the keywords that did NOT match). Both sorted by
overall match descending.

**Show both tables to the user verbatim, every resume row.** Do not truncate them, do
not add the matched keywords, do not add prose analysis. The only thing you may add is
one short closing line pointing to `/ats-deep <same posting>` for the full breakdown
(matched keywords, knockout gating, honest suggestions).

Then clean up `/tmp/ats_keywords.json` (the only temp file — `ats_score.py` is a
permanent part of the skill and must NOT be deleted).

Do NOT edit any resume and do NOT commit — this skill is read-only analysis.
