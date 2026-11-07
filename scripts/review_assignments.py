#!/usr/bin/env python3
"""Writes one review file per episode with every topic/language/exam/accent assignment and the
evidence behind it (mention count, title/show-notes hit, quote snippets), so a reviewer can judge
whether the assignment really makes sense.

Usage:  python scripts/review_assignments.py   -> data/review/assignments/<episode id>.md
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_wiki as b  # noqa: E402
from topics import TOPICS  # noqa: E402

OUT = b.DATA / "review" / "assignments"


def main() -> None:
    eps = b.load_episodes()
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for ep in eps:
        words = b.load_transcript(ep)
        if not words:
            continue
        words = b.content_words(words)
        text = " ".join(w["text"] for w in words)
        out = [f"# {ep['id']} – {ep['title']}", "", f"Show notes: {ep['description'][:600]}", "",
               "Columns: kind | name | status | evidence. Status: MAIN = main topic, MINOR = briefly mentioned.", ""]
        for topic in TOPICS:
            rx = re.compile("|".join(f"(?:{p})" for p in topic["patterns"]), re.IGNORECASE)
            in_title = bool(rx.search(ep["title"]))
            in_notes = in_title or bool(rx.search(b.notes_for_matching(ep["description"])))
            raw = len(rx.findall(text))
            min_main = max(topic.get("min", 0), b.FOLDER_MIN[topic["folder"]])
            notes_ok = in_title or (in_notes and raw >= b.MIN_NOTES[topic["folder"]])
            if (topic["name"], ep["id"]) in b.EXCLUDE:
                status = "EXCLUDED"
            elif notes_ok or raw >= min_main:
                status = "MAIN"
            elif raw >= b.FOLDER_MINOR[topic["folder"]]:
                status = "MINOR"
            else:
                continue
            quotes = b.find_quotes(words, topic["patterns"])[:4]
            why = ("title" if in_title else "show notes" if in_notes else "") + f" {raw} mentions"
            out.append(f"## {topic['folder']} | {topic['name']} | {status} | {why.strip()}")
            for q in quotes:
                out.append(f"- {b.fmt_time(q['t'])}: {q['quote']}")
            out.append("")
            n += 1
        (OUT / f"{ep['id']}.md").write_text("\n".join(out), encoding="utf-8")
    print(f"{n} assignments in {len(list(OUT.glob('*.md')))} files -> {OUT}")


if __name__ == "__main__":
    main()
