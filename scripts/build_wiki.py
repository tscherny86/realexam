#!/usr/bin/env python3
"""Builds the Real Exam English knowledge archive as an Obsidian vault.

Inputs (all in data/):
  feed.xml            – RSS feed of the podcast (all episodes, show notes, duration)
  spotify_ids.json    – episode label -> Spotify episode ID (for minute links)
  transcripts/*.json  – word-level transcripts, file name = episode ID (e.g. s06e10.json)
                        format: {"words": [{"text": "...", "start": 7.9, "end": 8.1}, ...]}
  official/*.txt      – official Buzzsprout transcripts (no timestamps), merged in by align_official.py
  corrections.tsv     – hearing-error corrections, applied while building
  topic_exclusions.tsv – hand-checked false topic assignments

Output: Real-Exam-English-Wiki/  (open this folder in Obsidian as a vault)

Usage:  python scripts/build_wiki.py
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import align_official  # noqa: E402
import corrections  # noqa: E402
from topics import TOPICS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
VAULT = ROOT / "Real-Exam-English-Wiki"
HOME = "Real Exam English Wiki"

NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd", "podcast": "https://podcastindex.org/namespace/1.0"}
SHOW_URL = "https://open.spotify.com/show/0aJJIQVuhGJcM7S2TJIjrW"
FOLDERS = ["Topics", "Language", "Exams", "Accents"]
# entries that are in nearly every episode -> episode level only, no quotes
NO_QUOTES: set[str] = set()
MAX_QUOTES_PER_EPISODE = 4
# topic -> episode (calibrated on the first 23 transcripts, 07.11.2026): the real subject of an episode is named
# 30–70 times, genuine side subjects 10–25 times, noise up to about 8. Language points, exams and accents are
# named explicitly by Trevor, so a few mentions are enough there.
#   main topic:        title hit, show-notes hit with at least MIN_NOTES mentions, or at least FOLDER_MIN mentions
#   briefly mentioned: at least FOLDER_MINOR mentions
# A topic entry may raise its own threshold with "min".
FOLDER_MIN = {"Topics": 10, "Language": 3, "Exams": 3, "Accents": 3}
FOLDER_MINOR = {"Topics": 4, "Language": 2, "Exams": 2, "Accents": 2}
MIN_NOTES = 3

CORRECTIONS: dict = {}  # episode -> Counter of applied correction rules
ALIGNMENT: dict = {}  # episode -> stats of the official-transcript alignment
_PR = DATA / "proofread.txt"
PROOFREAD = {l.split("\t")[0].strip() for l in (_PR.read_text(encoding="utf-8").splitlines() if _PR.exists() else []) if l.strip() and not l.startswith("#")}
_EXCL = DATA / "topic_exclusions.tsv"
EXCLUDE = {tuple(l.split("\t")[:2]) for l in (_EXCL.read_text(encoding="utf-8").splitlines() if _EXCL.exists() else []) if l and not l.startswith("#")}


# --------------------------------------------------------------------------- helpers
def fmt_time(sec: float) -> str:
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def clean_html(text: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", text or "")
    text = re.sub(r"</p>\s*<p>", "\n\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("�", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# Lines of the show notes that repeat in every episode (links, music credit, sponsor). They are removed
# from the displayed notes and ignored by the topic search.
BOILERPLATE = re.compile(
    r"^(For classes|For transcripts|For the Real Exam English app|Music:?\s|Link:|License:|Support the show|"
    r"Find your ideal English teacher|Links? to Cambridge|B2:|C1:|C2:|Link for Project Gutenberg)",
    re.I,
)


def strip_boilerplate(text: str) -> str:
    keep = [l for l in text.splitlines() if not BOILERPLATE.match(l.strip())]
    out = "\n".join(keep)
    out = re.sub(r"Support the show\s*$", "", out).strip()
    return re.sub(r"\n{3,}", "\n\n", out)


def safe_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|#^\[\]]', " ", name)
    return re.sub(r"\s+", " ", name).strip()


def parse_duration(d: str) -> int:
    parts = [int(p) for p in (d or "0").split(":")]
    sec = 0
    for p in parts:
        sec = sec * 60 + p
    return sec


# --------------------------------------------------------------------------- episodes
def load_episodes() -> list[dict]:
    root = ET.parse(DATA / "feed.xml").getroot()
    ids = json.loads((DATA / "spotify_ids.json").read_text(encoding="utf-8"))
    episodes = []
    for item in root.iter("item"):
        title = item.findtext("title").strip()
        date = parsedate_to_datetime(item.findtext("pubDate"))
        ep_type = item.findtext("itunes:episodeType", namespaces=NS) or "full"
        m = re.match(r"S(\d+)\s*-\s*(\d+)\s*(.*)", title)
        season = int(m.group(1)) if m else int(item.findtext("itunes:season", namespaces=NS) or 0)
        num = int(m.group(2)) if m else int(item.findtext("itunes:episode", namespaces=NS) or 0)
        if m and ep_type == "full":
            ep_id, key, short, kind = f"s{season:02d}e{num:02d}", f"S{season} E{num}", m.group(3).strip() or title, "episode"
        else:
            kind = "trailer" if ep_type == "trailer" else "bonus"
            ep_id, key, short, season, num = "x" + date.strftime("%Y-%m-%d"), kind.capitalize(), title, 0, 0
        enc = item.find("enclosure")
        tr = item.find("podcast:transcript", NS)
        guid = item.findtext("guid") or ""
        episodes.append(
            {
                "id": ep_id,
                "key": key,
                "kind": kind,
                "season": season,
                "num": num,
                "year": date.year,
                "title": title,
                "short": short,
                "date": date.strftime("%Y-%m-%d"),
                "duration": parse_duration(item.findtext("itunes:duration", namespaces=NS)),
                "description": strip_boilerplate(clean_html(item.findtext("description"))),
                "audio": enc.get("url", "") if enc is not None else "",
                "transcript_url": tr.get("url") if tr is not None else "",
                "buzzsprout_id": re.sub(r"\D", "", guid),
                "spotify_id": ids.get(key) if kind == "episode" else ids.get(title),
                "note": safe_filename(f"{ep_id} {short}"),
            }
        )
    episodes.sort(key=lambda e: (e["date"], e["id"]))
    return episodes


def spotify_link(ep: dict, sec: float | None = None) -> str:
    if ep["spotify_id"]:
        url = f"https://open.spotify.com/episode/{ep['spotify_id']}"
        return f"{url}?t={int(sec)}" if sec is not None else url
    return SHOW_URL


def load_transcript(ep: dict) -> list[dict] | None:
    f = DATA / "transcripts" / f"{ep['id']}.json"
    if not f.exists():
        return None
    data = json.loads(f.read_text(encoding="utf-8"))
    words = data["words"] if isinstance(data, dict) else data
    words = [w for w in words if w.get("type", "word") == "word" and w.get("text", "").strip()]
    words, hits = corrections.apply(words, ep["id"])
    CORRECTIONS[ep["id"]] = hits
    official = align_official.official_text(ep["id"])
    if official:
        words, stats = align_official.apply(words, official)
        ALIGNMENT[ep["id"]] = stats
    return words


def segments(words: list[dict], seconds: int = 60) -> list[dict]:
    """Groups words into paragraphs per minute (cut at the end of a sentence)."""
    segs, cur, start = [], [], None
    for w in words:
        if start is None:
            start = w["start"]
        cur.append(w["text"])
        bucket_full = w["end"] - start >= seconds
        if bucket_full and re.search(r"[.!?]\"?$", w["text"]) or w["end"] - start >= seconds * 1.5:
            segs.append({"start": start, "text": " ".join(cur)})
            cur, start = [], None
    if cur:
        segs.append({"start": start, "text": " ".join(cur)})
    return segs


def find_quotes(words: list[dict], patterns: list[str]) -> list[dict]:
    """Finds passages in the transcript; returns time + quote snippet."""
    if not words:
        return []
    import bisect

    text_parts, offsets, pos = [], [], 0
    for w in words:
        offsets.append(pos)
        text_parts.append(w["text"])
        pos += len(w["text"]) + 1
    full = " ".join(text_parts)
    hits, last_t = [], -999.0
    rx = re.compile("|".join(f"(?:{p})" for p in patterns), re.IGNORECASE)
    for m in rx.finditer(full):
        idx = bisect.bisect_right(offsets, m.start()) - 1
        t = words[idx]["start"]
        if t - last_t < 90:  # merge hits that are close together
            continue
        last_t = t
        lo, hi = max(0, idx - 12), min(len(words), idx + 22)
        snippet = " ".join(w["text"] for w in words[lo:hi])
        hits.append({"t": max(0.0, t - 3), "quote": ("… " if lo else "") + snippet + (" …" if hi < len(words) else "")})
    return hits


# --------------------------------------------------------------------------- writers
def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def sort_key(name: str, folder: str):
    return name.casefold()


def status_line(ep: dict, words) -> str:
    """Quality status of a transcript, shown on transcript and episode pages."""
    st = ALIGNMENT.get(ep["id"])
    if st and st.get("used"):
        return "aligned with the official transcript"
    if ep["id"] in PROOFREAD:
        return "fully proofread"
    return "**not yet proofread**"


def build() -> None:
    episodes = load_episodes()
    if VAULT.exists():
        for sub in ["Episodes", "Transcripts", *FOLDERS]:
            shutil.rmtree(VAULT / sub, ignore_errors=True)
    transcripts = {e["id"]: load_transcript(e) for e in episodes}
    n_tx = sum(1 for t in transcripts.values() if t)

    # ---- collect topic hits
    topic_hits: dict[str, list] = {}
    ep_topics: dict[str, dict[str, list[str]]] = {e["id"]: {f: [] for f in FOLDERS} for e in episodes}
    ep_mentions: dict[str, list[str]] = {e["id"]: [] for e in episodes}
    for topic in TOPICS:
        rx = re.compile("|".join(f"(?:{p})" for p in topic["patterns"]), re.IGNORECASE)
        min_mentions = max(topic.get("min", 0), FOLDER_MIN[topic["folder"]])
        min_minor = FOLDER_MINOR[topic["folder"]]
        hits = []
        for ep in episodes:
            in_title = bool(rx.search(ep["title"]))
            in_notes = in_title or bool(rx.search(re.sub(r"https?://\S+|www\.\S+", " ", ep["description"])))
            quotes = []
            words = transcripts[ep["id"]]
            if words and topic["name"] not in NO_QUOTES:
                quotes = find_quotes(words, topic["patterns"])
            raw = len(rx.findall(" ".join(w["text"] for w in words))) if words else 0
            if (topic["name"], ep["id"]) in EXCLUDE:
                continue
            # a show-notes hit counts only if the transcript backs it up (or there is no transcript yet)
            notes_ok = in_title or (in_notes and (not words or raw >= MIN_NOTES))
            if notes_ok or raw >= min_minor:
                main = notes_ok or raw >= min_mentions or topic["name"] in NO_QUOTES
                hits.append({"ep": ep, "in_notes": notes_ok, "quotes": quotes, "main": main, "raw": raw})
                if topic["name"] not in NO_QUOTES:
                    if main:
                        ep_topics[ep["id"]][topic["folder"]].append(topic["name"])
                    else:
                        ep_mentions[ep["id"]].append(topic["name"])
        topic_hits[topic["name"]] = hits

    # ---- episodes
    for ep in episodes:
        words = transcripts[ep["id"]]
        rows = "\n".join(
            f"| **{folder}** | {', '.join(f'[[{t}]]' for t in ep_topics[ep['id']][folder]) or '–'} |" for folder in FOLDERS
        )
        mentions_md = ", ".join(f"[[{t}]]" for t in ep_mentions[ep["id"]]) or "–"
        chapters = ""
        if words:
            segs = segments(words, 120)
            chapters = "\n## Chapters\n\n" + "\n".join(
                f"- [{fmt_time(s['start'])}]({spotify_link(ep, s['start'])}) – "
                f"{' '.join(s['text'].split()[:18])} … ([[Transcript {ep['id']}#Minute {int(s['start'] // 60)}|transcript]])"
                for s in segs
            )
        tx_line = (
            f"[[Transcript {ep['id']}]] (word-level timestamps, {status_line(ep, words)})"
            if words
            else "not transcribed yet – see [[How to Transcribe]]"
        )
        write(
            VAULT / "Episodes" / f"{ep['note']}.md",
            f"""---
type: episode
label: "{ep['key']}"
kind: {ep['kind']}
season: {ep['season']}
number: {ep['num']}
year: {ep['year']}
date: {ep['date']}
duration: "{fmt_time(ep['duration'])}"
spotify: "{spotify_link(ep)}"
transcript: {"true" if words else "false"}
tags: [episode, season-{ep['season']}]
---
# {ep['title']}

| | |
|---|---|
| **Date** | {ep['date']} |
| **Duration** | {fmt_time(ep['duration'])} |
| **Listen** | [Spotify]({spotify_link(ep)}) · [MP3]({ep['audio']}) |
| **Transcript** | {tx_line} |
{rows}
| **Briefly mentioned** | {mentions_md} |

## Show notes

{ep['description'] or '_no show notes_'}
{chapters}

---
← [[All Episodes]] · [[{HOME}|Home]]
""",
        )

        if words:
            segs = segments(words, 60)
            body = "\n\n".join(
                f"### Minute {int(s['start'] // 60)}\n[▶ {fmt_time(s['start'])}]({spotify_link(ep, s['start'])})  \n{s['text']}"
                for s in segs
            )
            write(
                VAULT / "Transcripts" / f"Transcript {ep['id']}.md",
                f"""---
type: transcript
label: "{ep['key']}"
tags: [transcript]
---
# Transcript – {ep['title']}

Episode: [[{ep['note']}]] · transcribed automatically, {status_line(ep, words)} ({sum(CORRECTIONS.get(ep['id'], {}).values())} corrections); occasional hearing errors are possible.
Click ▶ to open Spotify at exactly this point.

{body}
""",
            )

    # ---- topics / language / exams / accents
    for topic in TOPICS:
        hits = topic_hits[topic["name"]]
        quote_blocks, ep_list, ep_minor = [], [], []
        for h in hits:
            ep = h["ep"]
            mins = ", ".join(f"[{fmt_time(q['t'])}]({spotify_link(ep, q['t'])})" for q in h["quotes"][:MAX_QUOTES_PER_EPISODE])
            where = " · ".join(x for x in ["Show notes" if h["in_notes"] else "", f"Minute {mins}" if mins else ""] if x)
            (ep_list if h["main"] else ep_minor).append(f"- [[{ep['note']}|{ep['key']} – {ep['short']}]] ({ep['date']}) — {where}")
            for q in h["quotes"][:MAX_QUOTES_PER_EPISODE]:
                quote_blocks.append(
                    f"> {q['quote']}\n>\n> — [[{ep['note']}|{ep['key']}]], "
                    f"[Minute {fmt_time(q['t'])}]({spotify_link(ep, q['t'])}) · "
                    f"[[Transcript {ep['id']}#Minute {int(q['t'] // 60)}|in the transcript]]"
                )
        quotes_md = "\n## Said in the podcast\n\n" + "\n\n".join(quote_blocks) if quote_blocks else ""
        write(
            VAULT / topic["folder"] / f"{topic['name']}.md",
            f"""---
type: {topic['folder'].lower()}
episodes: {len(ep_list)}
tags: [{topic['folder'].lower()}]
---
# {topic['name']}

_{topic['summary']}_

## Background
{topic['body'].strip()}

> [!info] Note
> The background above is general knowledge. What is said **in the podcast** about it follows below,
> each passage linked to the exact minute.
{quotes_md}

## In these episodes ({len(ep_list)})

{chr(10).join(ep_list) or '_no episode yet where this was a main topic_'}
{f"{chr(10)}## Briefly mentioned ({len(ep_minor)}){chr(10)}{chr(10)}" + chr(10).join(ep_minor) + chr(10) if ep_minor else ""}
---
← [[{topic['folder']}]] · [[{HOME}|Home]]
""",
        )

    # ---- overviews
    by_season: dict[int, list] = {}
    for ep in episodes:
        by_season.setdefault(ep["season"], []).append(ep)
    eps_md = []
    for season in sorted(by_season, reverse=True):
        eps_md.append(f"## {'Season ' + str(season) if season else 'Bonus episodes'}\n")
        eps_md.append("| Episode | Date | Duration | Transcript |\n|---|---|---|---|")
        for ep in sorted(by_season[season], key=lambda e: (e["num"], e["date"]), reverse=True):
            eps_md.append(
                f"| [[{ep['note']}\\|{ep['key']} – {ep['short']}]] | {ep['date']} | {fmt_time(ep['duration'])} | "
                f"{'✅' if transcripts[ep['id']] else '–'} |"
            )
        eps_md.append("")
    write(VAULT / "All Episodes.md", "# All Episodes\n\n" + "\n".join(eps_md) + f"\n← [[{HOME}|Home]]")

    for folder in FOLDERS:
        items = sorted((t for t in TOPICS if t["folder"] == folder), key=lambda t: sort_key(t["name"], folder))
        lines = [f"- [[{t['name']}]] — {t['summary']} ({sum(h['main'] for h in topic_hits[t['name']])} episodes)" for t in items]
        write(VAULT / f"{folder}.md", f"# {folder}\n\n" + "\n".join(lines) + f"\n\n← [[{HOME}|Home]]")

    total = sum(e["duration"] for e in episodes)
    top = sorted(TOPICS, key=lambda t: -sum(h["main"] for h in topic_hits[t["name"]]))
    top_md = "\n".join(
        f"- [[{t['name']}]] ({sum(h['main'] for h in topic_hits[t['name']])})" for t in top if t["folder"] == "Topics"
    )
    latest = sorted(episodes, key=lambda e: e["date"], reverse=True)[:5]
    write(
        VAULT / f"{HOME}.md",
        f"""---
tags: [home]
---
# 🎧 Real Exam English Wiki – B2, C1, C2

The knowledge archive for the [Real Exam English podcast]({SHOW_URL}), in which Trevor asks native
English speakers exam-style questions and picks out the best language. Every piece of information is
linked to the **episode** – and, for transcribed episodes, to the **exact minute** (a click opens
Spotify at that point).

**Updated:** {datetime.now().strftime('%d.%m.%Y')} · **{len(episodes)} episodes** · **{total // 3600} h {total % 3600 // 60} min** of audio ·
**{n_tx} of {len(episodes)} transcribed**

## Navigation
- 📼 [[All Episodes]]
- 📚 [[Topics]] – exam topics with background and quotes
- 🔤 [[Language]] – grammar, vocabulary and pronunciation points
- 🎓 [[Exams]] – Cambridge, IELTS and exam skills
- 🌍 [[Accents]] – where the speakers come from
- 🛠️ [[How to Transcribe]] – add transcripts for further episodes

## Latest episodes
{chr(10).join(f"- [[{e['note']}|{e['title']}]] ({e['date']})" for e in latest)}

## Topics by frequency
{top_md}
""",
    )
    write(
        VAULT / "How to Transcribe.md",
        f"""# How to transcribe further episodes

Minute-exact links only exist for episodes with a transcript. This is how more are added:

## Option A – free, on your own PC (recommended)
1. Install Python 3.10+ and ffmpeg, then in the repo folder:
   ```
   pip install faster-whisper
   python scripts/transcribe_local.py
   python scripts/fetch_official.py
   python scripts/build_wiki.py
   ```
2. Obsidian updates itself – every topic article gets quotes with minute links.

Single episodes: `python scripts/transcribe_local.py s06e10 x2026-06-24`
With an NVIDIA graphics card the script uses the GPU (about 15× real time with `large-v3-turbo`).

## Option B – official transcripts
Buzzsprout publishes an official transcript for most episodes. `fetch_official.py` downloads them;
the build merges the official wording with the Whisper timestamps, so those transcripts count as
"aligned with the official transcript".

## Add Spotify links
For minute links on Spotify each episode needs its Spotify ID in `data/spotify_ids.json`
(the part after `/episode/` in the Spotify link). Without it the wiki links to the show.

← [[{HOME}|Home]]
""",
    )
    report = {k: {"total": sum(v.values()), "rules": dict(v.most_common())} for k, v in sorted(CORRECTIONS.items())}
    (DATA / "corrections_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    (DATA / "alignment_report.json").write_text(json.dumps(dict(sorted(ALIGNMENT.items())), ensure_ascii=False, indent=1), encoding="utf-8")
    (VAULT / ".obsidian").mkdir(exist_ok=True)
    (VAULT / ".obsidian" / "app.json").write_text(
        '{\n  "alwaysUpdateLinks": true,\n  "newFileLocation": "folder",\n  "newFileFolderPath": "Topics",\n  "showFrontmatter": false\n}\n',
        encoding="utf-8",
    )
    print(f"Vault built: {VAULT}  ({len(episodes)} episodes, {n_tx} transcripts, {len(TOPICS)} articles)")


if __name__ == "__main__":
    build()
