#!/usr/bin/env python3
"""Downloads the official episode transcripts that Buzzsprout publishes in the RSS feed
(<podcast:transcript url="…/transcript" type="text/html">) into data/official/<episode id>.txt.

Usage:  python scripts/fetch_official.py            # all episodes that have one and are not yet saved
        python scripts/fetch_official.py --force    # download again

The text is plain paragraphs without timestamps; align_official.py merges it with the Whisper
word timestamps while the wiki is built. 68 of the 75 episodes had one on 06.11.2026.
"""
import html
import re
import sys
import time
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):  # Windows console: allow ✓ and friends
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_wiki import DATA, load_episodes  # noqa: E402

OUT = DATA / "official"
UA = "Mozilla/5.0 (real-exam-english-fanwiki)"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")


def to_text(page: str) -> str:
    body = page.split("<body", 1)[-1]
    paras = re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)
    lines = []
    for p in paras:
        t = re.sub(r"<br\s*/?>", " ", p)
        t = html.unescape(re.sub(r"<[^>]+>", "", t))
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            lines.append(t)
    return "\n".join(lines)


def main() -> None:
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for ep in load_episodes():
        if not ep["transcript_url"]:
            continue
        target = OUT / f"{ep['id']}.txt"
        if target.exists() and not force:
            continue
        try:
            text = to_text(fetch(ep["transcript_url"]))
        except Exception as err:  # noqa: BLE001
            print(f"  ! {ep['id']}: {err}")
            continue
        if len(text.split()) < 50:
            print(f"  ! {ep['id']}: transcript page empty, skipped")
            continue
        target.write_text(text + "\n", encoding="utf-8")
        n += 1
        print(f"  ✓ {ep['id']}  {len(text.split())} words")
        time.sleep(0.5)
    print(f"{n} official transcripts saved, {len(list(OUT.glob('*.txt')))} in total")


if __name__ == "__main__":
    main()
