#!/usr/bin/env python3
"""Command "check": reload the RSS feed and report new or not yet transcribed episodes.

Usage:  python scripts/check_feed.py                 (downloads the feed)
        python scripts/check_feed.py --file X.xml     (feed from a file, e.g. a Firecrawl result
                                                       with "rawHtml" if buzzsprout is blocked)
Writes data/feed.xml only when it changed.
Output: one line per episode without a transcript, otherwise "no new episodes".
Exit code 0 = nothing to do, 10 = there are episodes to transcribe.
"""
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_URL = "https://feeds.buzzsprout.com/1107956.rss"
FEED = ROOT / "data" / "feed.xml"
sys.path.insert(0, str(ROOT / "scripts"))


def main() -> int:
    old = FEED.read_bytes() if FEED.exists() else b""
    if "--file" in sys.argv:
        raw = Path(sys.argv[sys.argv.index("--file") + 1]).read_text(encoding="utf-8")
        if raw.lstrip().startswith("{"):
            import json
            raw = json.loads(raw)["rawHtml"]
        new = raw.encode("utf-8")
    else:
        try:
            req = urllib.request.Request(FEED_URL, headers={"User-Agent": "real-exam-english-fanwiki/1.0"})
            new = urllib.request.urlopen(req, timeout=60).read()
        except OSError as err:
            print(f"Feed not reachable ({err}); fetch it another way and use --file", file=sys.stderr)
            return 2
    if b"<rss" not in new[:2000]:
        print("Feed could not be read", file=sys.stderr)
        return 2
    if new != old:
        FEED.write_bytes(new)
    import build_wiki as b  # import after writing so the new feed is used

    eps = b.load_episodes()
    missing = [e for e in eps if not (ROOT / "data" / "transcripts" / f"{e['id']}.json").exists()]
    print(f"Feed: {len(eps)} episodes{' (updated)' if new != old else ''}")
    if not missing:
        print("no new episodes")
        return 0
    for e in missing:
        print(f"NEW/NO TRANSCRIPT\t{e['id']}\t{e['date']}\t{e['title']}")
    return 10


if __name__ == "__main__":
    sys.exit(main())
