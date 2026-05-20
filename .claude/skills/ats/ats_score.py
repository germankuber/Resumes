#!/usr/bin/env python3
"""Deterministic ATS-style keyword scorer for the multi-resume repo.

Part of the /ats and /ats-deep skills. This script is FIXED — it does not change
per run. The skill only produces the keywords JSON and invokes this script.

Usage:
    python3 ats_score.py <keywords.json> [repo_root] [--json]

  <keywords.json>  path to the keyword spec produced by the skill (see SHAPE below)
  [repo_root]      repo root with one folder per resume, each holding a
                   "Germán Küber.html". Defaults to the current working directory.
  --json           emit the full JSON report instead of the colored table.
                   /ats uses the default (table); /ats-deep uses --json for detail.

Default output: a colored, box-drawn comparative table (Match % / Hard skills /
Title), resumes sorted by overall match descending. With --json: the full per-resume
report (overall %, sub-scores, matched list with exact/synonym tags, missing list).

keywords.json SHAPE:
{
  "job_title": "Senior Backend Engineer",
  "keywords": [
    {"term": "Rust", "category": "hard_skill", "frequency": 2, "synonyms": ["tokio"]},
    {"term": "Kubernetes", "category": "tool", "frequency": 1, "synonyms": ["K8s"]},
    {"term": "5+ years", "category": "qualification", "frequency": 1, "synonyms": [],
     "qualification_kind": "years_experience", "value": 5}
  ]
}

category is one of: hard_skill, tool, title, other_keyword, soft_skill, qualification.
"qualification" keywords are NOT scored in the % — the skill gates them separately.
"""
import json
import os
import re
import sys

WEIGHTS = {"hard_skill": 3, "tool": 3, "title": 3, "other_keyword": 2, "soft_skill": 1}
RESUME_FILENAME = "Germán Küber.html"

# ANSI colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"


def color_for_pct(pct: int) -> str:
    """Green >=75, yellow 50-74, red <50 — Jobscan-style thresholds."""
    if pct >= 75:
        return GREEN
    if pct >= 50:
        return YELLOW
    return RED


def strip_html(html: str) -> str:
    """Reduce resume HTML to lowercased plain text for substring matching."""
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = (text.replace("&amp;", "&").replace("&lt;", "<")
                .replace("&gt;", ">").replace("&nbsp;", " "))
    return re.sub(r"\s+", " ", text).lower()


def list_resumes(repo_root: str):
    """Return [(folder_name, html_path)] for every resume folder in the repo."""
    out = []
    for d in sorted(os.listdir(repo_root)):
        p = os.path.join(repo_root, d)
        if os.path.isdir(p) and not d.startswith(".") and d != ".git":
            f = os.path.join(p, RESUME_FILENAME)
            if os.path.exists(f):
                out.append((d, f))
    return out


def classify(kw: dict, text: str):
    """Return (match_tag, credit) for one keyword against one resume's text."""
    term = kw["term"].lower()
    if term in text:
        return "exact", 1.0
    for syn in kw.get("synonyms", []):
        if syn.lower() in text:
            return "synonym:" + syn, 0.9
    return "absent", 0.0


def score_resume(name: str, html_path: str, scored_kws: list) -> dict:
    text = strip_html(open(html_path, encoding="utf-8").read())
    tot_w = got_w = 0.0
    cat_tot: dict = {}
    cat_got: dict = {}
    matched, missing = [], []
    for kw in scored_kws:
        cat = kw["category"]
        w = WEIGHTS[cat] * min(kw.get("frequency", 1), 3)
        tag, credit = classify(kw, text)
        tot_w += w
        got_w += w * credit
        cat_tot[cat] = cat_tot.get(cat, 0.0) + w
        cat_got[cat] = cat_got.get(cat, 0.0) + w * credit
        entry = {"term": kw["term"], "category": cat}
        if credit > 0:
            matched.append({**entry, "match": tag})
        else:
            missing.append(entry)
    overall = round(got_w / tot_w * 100) if tot_w else 0
    subs = {c: round(cat_got[c] / cat_tot[c] * 100) for c in cat_tot if cat_tot[c]}
    return {"resume": name, "overall": overall, "subscores": subs,
            "matched": matched, "missing": missing}


def render_table(results: list, job_title: str) -> str:
    """Box-drawn, colored comparative table: Resume / Match% / Hard skills / Title."""
    headers = ["Resume", "Match %", "Hard skills", "Title"]
    rows = []
    for r in results:
        subs = r["subscores"]
        rows.append([
            r["resume"],
            "{}%".format(r["overall"]),
            "{}%".format(subs.get("hard_skill", 0)) if "hard_skill" in subs else "—",
            "{}%".format(subs.get("title", 0)) if "title" in subs else "—",
        ])
    # column widths from plain (uncolored) text
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def hline(left, mid, right):
        return left + mid.join("─" * (w + 2) for w in widths) + right

    def fmt_row(cells, colors=None):
        parts = []
        for i, cell in enumerate(cells):
            pad = " " * (widths[i] - len(cell))
            c = colors[i] if colors else ""
            reset = RESET if c else ""
            parts.append(" " + c + cell + reset + pad + " ")
        return "│" + "│".join(parts) + "│"

    out = []
    title = job_title or "job posting"
    out.append(BOLD + CYAN + "ATS keyword-match — " + title + RESET)
    out.append(DIM + "Scanner-style estimate, not a real ATS score." + RESET)
    out.append("")
    out.append(hline("┌", "┬", "┐"))
    out.append(fmt_row(headers, [BOLD] * len(headers)))
    out.append(hline("├", "┼", "┤"))
    for idx, (r, row) in enumerate(zip(results, rows)):
        oc = color_for_pct(r["overall"])
        hc = color_for_pct(r["subscores"].get("hard_skill", 0))
        tc = color_for_pct(r["subscores"].get("title", 0))
        out.append(fmt_row(row, ["", oc + BOLD, hc, tc]))
        if idx < len(rows) - 1:
            out.append(hline("├", "┼", "┤"))
    out.append(hline("└", "┴", "┘"))
    out.append("")
    out.append(DIM + "green ≥75%  ·  yellow 50–74%  ·  red <50%   "
               "(threshold for a strong match: 75%)" + RESET)
    return "\n".join(out)


def render_keyword_list(scored_kws: list) -> str:
    """The set of keywords being analyzed, grouped by category."""
    by_cat: dict = {}
    for kw in scored_kws:
        by_cat.setdefault(kw["category"], []).append(kw["term"])
    order = ["title", "hard_skill", "tool", "other_keyword", "soft_skill"]
    labels = {"title": "Title", "hard_skill": "Hard skills", "tool": "Tools",
              "other_keyword": "Other keywords", "soft_skill": "Soft skills"}
    out = [BOLD + "Keywords analyzed ({})".format(len(scored_kws)) + RESET]
    for cat in order:
        if cat in by_cat:
            terms = ", ".join(by_cat[cat])
            out.append("  " + DIM + labels[cat] + ":" + RESET + " " + terms)
    return "\n".join(out)


def render_detail(results: list) -> str:
    """Per-resume two-column breakdown: matched (✅) | missing (❌)."""
    out = [BOLD + "Per-resume keyword breakdown" + RESET]
    for r in results:
        matched = [m["term"] + ("  ≈" if m["match"].startswith("synonym") else "")
                   for m in r["matched"]]
        missing = [m["term"] for m in r["missing"]]
        n = max(len(matched), len(missing))
        left_w = max([len(x) for x in matched] + [14])
        oc = color_for_pct(r["overall"])
        out.append("")
        out.append(oc + BOLD + "▸ " + r["resume"]
                   + "  ({}%)".format(r["overall"]) + RESET)
        out.append("  " + GREEN + "✅ matched ({})".format(len(matched)) + RESET
                   + " " * (left_w - 12) + "  "
                   + RED + "❌ missing ({})".format(len(missing)) + RESET)
        for i in range(n):
            lt = matched[i] if i < len(matched) else ""
            rt = missing[i] if i < len(missing) else ""
            lcell = GREEN + lt + RESET if lt else ""
            pad = " " * (left_w - len(lt))
            rcell = RED + rt + RESET if rt else ""
            out.append("  " + lcell + pad + "  " + rcell)
    out.append("")
    out.append(DIM + "≈ = matched via a synonym/variant, not the exact phrase" + RESET)
    return "\n".join(out)


def render_missing_table(results: list) -> str:
    """Compact summary table: Resume | keywords that did NOT match."""
    rows = []
    for r in results:
        missing = ", ".join(m["term"] for m in r["missing"]) or "—"
        rows.append([r["resume"], missing])
    name_w = max([len(r[0]) for r in rows] + [len("Resume")])
    # wrap the missing column to keep the table readable
    miss_w = 64

    def wrap(text, width):
        words = text.split(", ")
        lines, cur = [], ""
        for w in words:
            piece = w if not cur else cur + ", " + w
            if len(piece) > width and cur:
                lines.append(cur)
                cur = w
            else:
                cur = piece
        if cur:
            lines.append(cur)
        return lines or [""]

    def hline(left, mid, right):
        return left + "─" * (name_w + 2) + mid + "─" * (miss_w + 2) + right

    out = [BOLD + "Missing keywords by resume" + RESET, ""]
    out.append(hline("┌", "┬", "┐"))
    out.append("│ " + BOLD + "Resume".ljust(name_w) + RESET
               + " │ " + BOLD + "Missing keywords".ljust(miss_w) + RESET + " │")
    out.append(hline("├", "┼", "┤"))
    for idx, (name, missing) in enumerate(rows):
        wrapped = wrap(missing, miss_w)
        for j, line in enumerate(wrapped):
            left = name if j == 0 else ""
            out.append("│ " + left.ljust(name_w) + " │ "
                       + RED + line + RESET + " " * (miss_w - len(line)) + " │")
        if idx < len(rows) - 1:
            out.append(hline("├", "┼", "┤"))
    out.append(hline("└", "┴", "┘"))
    return "\n".join(out)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    if not args:
        sys.exit("usage: python3 ats_score.py <keywords.json> [repo_root] [--json]")
    spec = json.load(open(args[0], encoding="utf-8"))
    repo_root = args[1] if len(args) > 1 else os.getcwd()
    scored_kws = [k for k in spec["keywords"] if k["category"] != "qualification"]
    resumes = list_resumes(repo_root)
    if not resumes:
        sys.exit("no resume folders found under: " + repo_root)
    results = [score_resume(n, p, scored_kws) for n, p in resumes]
    results.sort(key=lambda r: r["overall"], reverse=True)
    if "--json" in flags:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(render_keyword_list(scored_kws))
        print()
        print(render_table(results, spec.get("job_title", "")))
        print()
        print(render_detail(results))
        print()
        print(render_missing_table(results))


if __name__ == "__main__":
    main(sys.argv)
