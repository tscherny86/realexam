#!/usr/bin/env python3
"""Quality scan of the final transcripts (after alignment and corrections).

Flags passages that look like transcription damage so a proofreader can look there first:
  - a word repeated twice in a row ("the the")
  - tokens with letters glued to punctuation or digits ("word.Another", "B -2")
  - rare words: appear in only one transcript and never in an official transcript (likely mishearings)
  - non-ASCII characters apart from common punctuation
  - very long gaps between consecutive words (> 20 s) – a sign of lost audio or wrong timestamps

Usage:  python scripts/qa_scan.py            -> data/review/scan.md (one section per episode)
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_wiki as b  # noqa: E402

OUT = b.DATA / "review"
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
COMMON_OK = set("ok okay yeah gonna wanna gotta kinda sorta dunno hmm mm uh um ah oh".split())


def main() -> None:
    eps = b.load_episodes()
    tx = {e["id"]: b.load_transcript(e) for e in eps}
    official_vocab: set[str] = set()
    for f in b.align_official.OFFICIAL.glob("*.txt"):
        official_vocab.update(w.lower() for w in WORD.findall(f.read_text(encoding="utf-8")))
    df: Counter = Counter()
    per_ep: dict[str, Counter] = {}
    for eid, words in tx.items():
        if not words:
            continue
        c = Counter(w.lower() for t in words for w in WORD.findall(t["text"]))
        per_ep[eid] = c
        df.update(c.keys())
    OUT.mkdir(parents=True, exist_ok=True)
    lines = ["# QA scan of all transcripts (after alignment and corrections)", ""]
    total = 0
    for ep in eps:
        words = tx[ep["id"]]
        if not words:
            continue
        flags = []
        prev = None
        for i, w in enumerate(words):
            t = w["text"]
            core = t.strip(".,!?;:\"'()[]…–-")
            if prev and core and core.lower() == prev.lower() and core.isalpha() and len(core) > 2:
                flags.append((w["start"], f"repeated word: “{prev} {t}”"))
            if re.search(r"[A-Za-z][.!?][A-Za-z]", t) or re.search(r"\s-\w|\w -\w", t):
                flags.append((w["start"], f"glued/split token: “{t}”"))
            if re.search(r"[^\x00-\x7F’“”…–—£€]", t):
                flags.append((w["start"], f"unusual character: “{t}”"))
            if i and w["start"] - words[i - 1]["end"] > 20:
                flags.append((w["start"], f"gap of {w['start'] - words[i-1]['end']:.0f} s before “{t}”"))
            prev = core
        rare = sorted(w for w, n in per_ep[ep["id"]].items() if df[w] == 1 and w not in official_vocab
                      and w not in COMMON_OK and len(w) > 3 and n == 1)
        aligned = b.ALIGNMENT.get(ep["id"], {}).get("used")
        lines.append(f"## {ep['id']} – {ep['title']} ({'aligned with official transcript' if aligned else 'Whisper only, proofread by hand'})")
        for s, msg in sorted(flags)[:40]:
            lines.append(f"- {b.fmt_time(s)}: {msg}")
        if rare:
            lines.append(f"- rare words (only here, not in any official transcript): {', '.join(rare[:40])}")
        if not flags and not rare:
            lines.append("- nothing flagged")
        lines.append("")
        total += len(flags)
    (OUT / "scan.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{total} flags -> {OUT / 'scan.md'}")


if __name__ == "__main__":
    main()
