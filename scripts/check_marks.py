#!/usr/bin/env python3
"""Checks that the minute marks really point to the words they claim.

For a sample of positions per episode it cuts a few seconds of audio at the timestamp, transcribes
that clip with Whisper and compares it with the transcript words around the same timestamp.
A low similarity means the timestamp (or the aligned text there) is off.

Usage:  python scripts/check_marks.py            # 4 samples per episode
        python scripts/check_marks.py --per 8    # more samples
        python scripts/check_marks.py s06e10     # only these episodes
Output: data/review/marks.md and a one-line summary. Audio is cached in data/review/audio/.
"""
import argparse
import difflib
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_wiki as b  # noqa: E402
from transcribe_local import UA, add_cuda_dlls  # noqa: E402

CLIP = 8.0  # seconds
OUT = b.DATA / "review"
CACHE = OUT / "audio"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", s.lower().replace("’", "'"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--per", type=int, default=4)
    args = ap.parse_args()
    add_cuda_dlls()
    from faster_whisper import WhisperModel

    try:
        model = WhisperModel("large-v3-turbo", device="cuda", compute_type="float16")
    except Exception:  # noqa: BLE001
        model = WhisperModel("small", device="cpu", compute_type="int8")
    CACHE.mkdir(parents=True, exist_ok=True)
    rows, bad = [], 0
    for ep in b.load_episodes():
        if args.ids and ep["id"] not in args.ids:
            continue
        words = b.load_transcript(ep)
        if not words or len(words) < 200:
            continue
        mp3 = CACHE / f"{ep['id']}.mp3"
        if not mp3.exists():
            req = urllib.request.Request(ep["audio"], headers={"User-Agent": UA})
            mp3.write_bytes(urllib.request.urlopen(req, timeout=120).read())
        dur = words[-1]["end"]
        # evenly spread sample points, away from the very start and end
        points = [dur * (k + 1) / (args.per + 1) for k in range(args.per)]
        for t in points:
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t:.2f}", "-t", str(CLIP), "-i", str(mp3),
                                  "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
            audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
            segs, _ = model.transcribe(audio, language="en", vad_filter=False)
            heard = norm(" ".join(s.text for s in segs))
            expected = norm(" ".join(w["text"] for w in words if t - 1 <= w["start"] <= t + CLIP + 1))
            ratio = difflib.SequenceMatcher(None, heard.split(), expected.split(), autojunk=False).ratio()
            ok = ratio >= 0.5 or (heard and heard.split()[:3] == expected.split()[:3])
            if not ok:
                bad += 1
            rows.append((ep["id"], t, ratio, ok, heard[:90], expected[:90]))
            print(f"{'ok ' if ok else 'BAD'} {ep['id']} {b.fmt_time(t)} {ratio:.2f}", flush=True)
    lines = ["# Audio mark check", "", f"{len(rows)} samples, {bad} mismatches (similarity < 0.5)", ""]
    for eid, t, r, ok, heard, exp in rows:
        if not ok:
            lines += [f"## {eid} {b.fmt_time(t)} – similarity {r:.2f}", f"- heard:    {heard}", f"- expected: {exp}", ""]
    (OUT / "marks.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(rows)} samples, {bad} mismatches -> {OUT / 'marks.md'}")


if __name__ == "__main__":
    main()
