"""Guard tests for ats_score.classify() separator normalization.

Run: python3 -m pytest .claude/skills/ats/test_ats_score.py
"""
from ats_score import classify, normalize_seps


def _kw(term, synonyms=None):
    return {"term": term, "category": "hard_skill", "synonyms": synonyms or []}


# --- normalize_seps: separators that MUST collapse -------------------------
def test_hyphen_collapses():
    assert normalize_seps("problem-solving") == "problem solving"


def test_slash_collapses():
    assert normalize_seps("CI/CD") == "ci cd"


def test_underscore_collapses():
    assert normalize_seps("real_time") == "real time"


def test_whitespace_runs_collapse():
    assert normalize_seps("CI  /  CD") == "ci cd"


# --- normalize_seps: characters that MUST be preserved ---------------------
def test_plus_preserved():
    assert normalize_seps("C++") == "c++"


def test_hash_preserved():
    assert normalize_seps("C#") == "c#"


def test_dot_preserved():
    assert normalize_seps(".NET") == ".net"


# --- classify: cross-variant matching --------------------------------------
def test_match_across_separator_variants():
    text = normalize_seps("strong problem solving and ci-cd pipelines")
    assert classify(_kw("problem-solving"), text) == ("exact", 1.0)
    assert classify(_kw("CI/CD"), text) == ("exact", 1.0)


def test_synonym_normalized_too():
    text = normalize_seps("we use k8s in prod")
    tag, credit = classify(_kw("Kubernetes", ["K8s"]), text)
    assert tag == "synonym:K8s" and credit == 0.9


def test_absent_keyword():
    text = normalize_seps("python and rust only")
    assert classify(_kw("Kubernetes"), text) == ("absent", 0.0)


def test_cpp_not_confused_with_c():
    text = normalize_seps("experienced in c++ systems")
    assert classify(_kw("C++"), text) == ("exact", 1.0)
