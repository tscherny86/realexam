"""Aligns the automatic (Whisper) transcript with the official Buzzsprout transcript.

Whisper gives us word timestamps but mishears words; the official transcript (data/official/<id>.txt,
fetched by fetch_official.py) has the correct words but no timestamps. This module merges both:

- words that match keep their Whisper timestamp and take the official spelling/punctuation,
- runs of words that differ are replaced by the official words, timed evenly across the span
  Whisper heard,
- words Whisper invented are dropped, words it missed are inserted with interpolated times.

Result: the official text, minute by minute. apply() returns (words, stats) where stats holds the
share of words that matched (a low ratio means the official transcript probably belongs to a
different cut of the episode and the alignment is not trusted).
"""
import difflib
import re
from pathlib import Path

OFFICIAL = Path(__file__).resolve().parent.parent / "data" / "official"
MIN_RATIO = 0.6  # below this the official text is ignored
LONG_RUN = 25  # runs longer than this are passages the official text lacks or moved, not hearing errors

_NORM = re.compile(r"[^a-z0-9']+")


def norm(s: str) -> str:
    return _NORM.sub("", s.lower().replace("’", "'"))


def tokens(text: str) -> list[str]:
    return [t for t in text.replace(" ", " ").split() if norm(t)]


def official_text(ep_id: str) -> str | None:
    f = OFFICIAL / f"{ep_id}.txt"
    return f.read_text(encoding="utf-8") if f.exists() else None


def _spread(items: list[str], start: float, end: float) -> list[dict]:
    """Distributes words evenly between start and end."""
    n = len(items)
    if n == 0:
        return []
    step = max(0.0, (end - start)) / n
    out = []
    for k, t in enumerate(items):
        s = round(start + k * step, 2)
        out.append({"text": t, "type": "word", "start": s, "end": round(s + step, 2)})
    return out


def apply(words: list[dict], text: str):
    """Returns (aligned words, {"ratio": matched share, "replaced": n, "inserted": n, "deleted": n})."""
    off = tokens(text)
    if not words or not off:
        return words, {"ratio": 0.0}
    a = [norm(w["text"]) for w in words]
    b = [norm(t) for t in off]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out, matched, rep, ins, dele = [], 0, 0, 0, 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                out.append({**words[i], "text": off[j]})
            matched += i2 - i1
        elif tag == "replace":
            out.extend(_spread(off[j1:j2], words[i1]["start"], words[i2 - 1]["end"]))
            rep += j2 - j1
        elif tag == "insert":
            if j2 - j1 > LONG_RUN:  # a whole passage the official text has elsewhere: timing unknown, skip
                continue
            prev_end = out[-1]["end"] if out else (words[i1]["start"] if i1 < len(words) else 0.0)
            next_start = words[i1]["start"] if i1 < len(words) else prev_end + 0.3 * (j2 - j1)
            out.extend(_spread(off[j1:j2], prev_end, max(next_start, prev_end)))
            ins += j2 - j1
        elif tag == "delete":
            if i2 - i1 > LONG_RUN:  # a whole passage missing from the official text: keep what Whisper heard
                out.extend(words[i1:i2])
                continue
            dele += i2 - i1
    ratio = matched / max(1, len(a))
    if ratio < MIN_RATIO:
        return words, {"ratio": round(ratio, 3), "used": False}
    return out, {"ratio": round(ratio, 3), "replaced": rep, "inserted": ins, "deleted": dele, "used": True}
