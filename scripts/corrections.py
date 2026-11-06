"""Fixes typical transcription errors of the automatic transcript (e.g. "Trevor" heard as "Trever").

The rules live in data/corrections.tsv (one rule per line, tab-separated):
    WRONG <Tab> RIGHT <Tab> global|local <Tab> episodes (local only, e.g. s03e02,x2024-05-01)

- WRONG may consist of several words ("real exam Inglish").
- Matching is whole-word and case-insensitive; punctuation at the edges is kept.
- "global" applies to every transcript (including future ones), "local" only to the listed episodes.

The raw data in data/transcripts/ stays untouched; corrections are applied while the wiki is built.
Episodes that have an official Buzzsprout transcript are additionally aligned to that text
(see align_official.py), which fixes most hearing errors on its own.
"""
import re
from collections import Counter
from pathlib import Path

RULES_FILE = Path(__file__).resolve().parent.parent / "data" / "corrections.tsv"
EDGE = re.compile(r"^([^\w]*)(.*?)([^\w%]*)$", re.S)


def _key(text: str) -> str:
    return " ".join(text.lower().split())


def load_rules():
    """-> {word count: {wrong_lower: [(right, None | set(episodes)), ...]}}"""
    rules = {}
    if not RULES_FILE.exists():
        return rules
    for line in RULES_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        wrong, right = parts[0].strip(), parts[1].strip()
        scope = parts[2].strip() if len(parts) > 2 else "global"
        eps = None if scope == "global" else {e.strip() for e in (parts[3] if len(parts) > 3 else "").split(",") if e.strip()}
        if wrong and right and _key(wrong) != _key(right):
            rules.setdefault(len(wrong.split()), {}).setdefault(_key(wrong), []).append((right, eps))
    return rules


RULES = load_rules()
MAXN = max(RULES, default=0)


def apply(words: list[dict], ep_id: str):
    """Returns (corrected words, Counter{"wrong → right": count})."""
    out, hits, i = [], Counter(), 0
    while i < len(words):
        done = False
        for n in range(min(MAXN, len(words) - i), 0, -1):
            table = RULES.get(n)
            if not table:
                continue
            chunk = words[i:i + n]
            m = EDGE.match(" ".join(w["text"] for w in chunk))
            lead, core, trail = m.group(1), m.group(2), m.group(3)
            cands = table.get(_key(core), [])
            # episode-specific rule beats the global one
            right = next((r for r, eps in cands if eps is not None and ep_id in eps), None) \
                or next((r for r, eps in cands if eps is None), None)
            if not right:
                continue
            if core[:1].isupper() and right[:1].islower() and right[1:] == right[1:].lower():  # keep sentence start
                right = right[0].upper() + right[1:]
            out.append({**chunk[0], "text": lead + right + trail, "end": chunk[-1]["end"]})
            hits[f"{core} → {right}"] += 1
            i += n
            done = True
            break
        if not done:
            out.append(words[i])
            i += 1
    return out, hits
