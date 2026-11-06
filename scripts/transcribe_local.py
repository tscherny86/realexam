#!/usr/bin/env python3
"""Transcribes Real Exam English episodes for free on your own PC (faster-whisper).

One-time setup:
    pip install faster-whisper
    (NVIDIA GPU: pip install nvidia-cublas-cu12 nvidia-cudnn-cu12 – the script finds the DLLs itself)
    ffmpeg must be on the PATH.

Usage (in the repo folder):
    python scripts/transcribe_local.py                  # all episodes without a transcript, newest first
    python scripts/transcribe_local.py s06e10 x2026-06-24   # only these episodes
    python scripts/transcribe_local.py --model small     # faster, less accurate (default: large-v3-turbo)
    python scripts/transcribe_local.py --cpu             # force CPU

Afterwards:  python scripts/build_wiki.py   -> the wiki is rebuilt with minute links.

On an RTX 3070 the default model runs at about 15× real time; on a CPU expect roughly real time
with "small". Progress is saved every 15 segments (data/transcripts/partial/), so an interrupted
run continues where it stopped.
"""
import argparse
import glob
import json
import os
import site
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import numpy as np

if hasattr(sys.stdout, "reconfigure"):  # Windows console: allow ▶ ✓ ↻
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_wiki import DATA, load_episodes  # noqa: E402

UA = "Mozilla/5.0 (real-exam-english-fanwiki)"


def add_cuda_dlls() -> None:
    """Makes the pip-installed CUDA libraries (cublas, cudnn) visible on Windows."""
    for s in site.getsitepackages() + [site.getusersitepackages()]:
        for d in glob.glob(os.path.join(s, "nvidia", "*", "bin")):
            if hasattr(os, "add_dll_directory"):
                os.add_dll_directory(d)
            os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*", help="episode IDs such as s06e10 (empty = all missing)")
    ap.add_argument("--model", default="large-v3-turbo", help="tiny | base | small | medium | large-v3 | large-v3-turbo")
    ap.add_argument("--cpu", action="store_true", help="force CPU")
    ap.add_argument("--push", action="store_true", help="rebuild the wiki, commit and push after every episode")
    args = ap.parse_args()

    add_cuda_dlls()
    from faster_whisper import WhisperModel

    try:
        if args.cpu:
            raise RuntimeError("cpu requested")
        model = WhisperModel(args.model, device="cuda", compute_type="float16")
        print(f"model {args.model} on GPU", flush=True)
    except Exception as err:  # noqa: BLE001
        print(f"GPU not available ({err}); using CPU", flush=True)
        model = WhisperModel(args.model, device="cpu", compute_type="int8")
    out_dir = DATA / "transcripts"
    out_dir.mkdir(parents=True, exist_ok=True)

    # newest episodes first
    for ep in sorted(load_episodes(), key=lambda e: e["date"], reverse=True):
        target = out_dir / f"{ep['id']}.json"
        if args.ids and ep["id"] not in args.ids:
            continue
        if not args.ids and target.exists():
            continue
        print(f"▶ {ep['id']}  {ep['title']}", flush=True)
        partial = out_dir / "partial" / f"{ep['id']}.json"
        partial.parent.mkdir(exist_ok=True)
        words = json.loads(partial.read_text(encoding="utf-8"))["words"] if partial.exists() else []
        offset = words[-1]["end"] if words else 0.0
        if offset:
            print(f"   ↻ resuming at {offset:.0f}s", flush=True)
        with tempfile.TemporaryDirectory() as tmp:
            mp3 = Path(tmp) / "audio.mp3"
            req = urllib.request.Request(ep["audio"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r, open(mp3, "wb") as f:
                f.write(r.read())
            raw = subprocess.run(
                ["ffmpeg", "-loglevel", "error", "-ss", str(offset), "-i", str(mp3), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                capture_output=True, check=True,
            ).stdout
            audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
            segs, _ = model.transcribe(audio, language="en", word_timestamps=True, vad_filter=True)
            for n, seg in enumerate(segs):
                for w in seg.words or []:
                    words.append({"text": w.word.strip(), "type": "word",
                                  "start": round(w.start + offset, 2), "end": round(w.end + offset, 2)})
                print(f"   {seg.start + offset:7.0f}s  {seg.text[:70]}", flush=True)
                if n % 15 == 0:
                    partial.write_text(json.dumps({"words": words}, ensure_ascii=False), encoding="utf-8")
        target.write_text(json.dumps({"words": words}, ensure_ascii=False), encoding="utf-8")
        partial.unlink(missing_ok=True)
        print(f"   ✓ {len(words)} words -> {target.name}", flush=True)
        if args.push:
            root = Path(__file__).resolve().parent.parent
            subprocess.run([sys.executable, str(root / "scripts" / "build_wiki.py")], check=True)
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", f"Transcript {ep['id']}: {ep['title']}\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"], check=False)
            for _ in range(4):
                if subprocess.run(["git", "-C", str(root), "push", "-q", "origin", "HEAD"]).returncode == 0:
                    break


if __name__ == "__main__":
    main()
