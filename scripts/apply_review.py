#!/usr/bin/env python3
"""Merges the reviewers' findings (data/review/out/proof-*.tsv, assign-*.tsv) into the rule files.

- proof-*.tsv: WRONG<TAB>RIGHT<TAB>global|local<TAB>episode<TAB>reason → data/corrections.tsv
  A rule is only taken over if WRONG really occurs in the final transcript of that episode (whole words,
  case-insensitive) and the correction is not already known. Rules that would not fire are listed.
- assign-*.tsv: NAME<TAB>episode<TAB>reason → data/topic_exclusions.tsv
  Only names that exist in scripts/topics.py and known episode IDs are taken over.

Usage:  python scripts/apply_review.py            # report only
        python scripts/apply_review.py --write    # append the valid rules
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_wiki as b  # noqa: E402
from topics import TOPICS  # noqa: E402

OUT = b.DATA / "review" / "out"
NAMES = {t["name"] for t in TOPICS}


def norm(s: str) -> str:
    return " ".join(re.sub(r"[^\w' ]+", " ", s.lower().replace("’", "'")).split())


def main() -> None:
    write = "--write" in sys.argv
    eps = {e["id"]: e for e in b.load_episodes()}
    texts = {}

    def text(eid):
        if eid not in texts:
            w = b.load_transcript(eps[eid]) or []
            texts[eid] = " " + norm(" ".join(x["text"] for x in w)) + " "
        return texts[eid]

    existing = {l.split("\t")[0].strip().lower() + "|" + (l.split("\t") + ["", "", ""])[3].strip()
                for l in (b.DATA / "corrections.tsv").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
    good, bad, dup = [], [], []
    for f in sorted(OUT.glob("proof-*.tsv")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#") or line.lower().startswith("wrong\t"):
                continue
            p = [x.strip() for x in line.split("\t")] + ["", "", "", ""]
            wrong, right, scope, eid, reason = p[0], p[1], (p[2] or "local").lower(), p[3], p[4]
            if not wrong or not right or norm(wrong) == norm(right):
                continue
            if scope == "global":
                where = [e for e in eps if (" " + norm(wrong) + " ") in text(e)]
                ok = bool(where)
            else:
                ok = eid in eps and (" " + norm(wrong) + " ") in text(eid)
            key = wrong.lower() + "|" + (eid if scope == "local" else "")
            if key in existing:
                dup.append((wrong, right, eid))
            elif ok:
                good.append((wrong, right, scope, eid if scope == "local" else "", reason, f.name))
                existing.add(key)
            else:
                bad.append((wrong, right, eid, f.name))
    excl_existing = {tuple(l.split("\t")[:2]) for l in (b.DATA / "topic_exclusions.tsv").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
    ex_good, ex_bad = [], []
    for f in sorted(OUT.glob("assign-*.tsv")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            p = [x.strip() for x in line.split("\t")] + ["", ""]
            name, eid, reason = p[0], p[1], p[2]
            if name in NAMES and eid in eps and (name, eid) not in excl_existing:
                ex_good.append((name, eid, reason)); excl_existing.add((name, eid))
            elif (name, eid) not in excl_existing:
                ex_bad.append((name, eid, f.name))
    print(f"corrections: {len(good)} valid, {len(bad)} not found in transcript, {len(dup)} already known")
    for w, r, e, f in bad[:40]:
        print(f"  NOT FOUND [{f} {e}] {w!r} -> {r!r}")
    print(f"exclusions: {len(ex_good)} valid, {len(ex_bad)} unknown name/episode")
    for n, e, f in ex_bad[:40]:
        print(f"  UNKNOWN [{f}] {n!r} {e}")
    if write:
        with open(b.DATA / "corrections.tsv", "a", encoding="utf-8") as fh:
            for w, r, s, e, reason, _ in good:
                fh.write(f"{w}\t{r}\t{s}\t{e}\n")
        with open(b.DATA / "topic_exclusions.tsv", "a", encoding="utf-8") as fh:
            for n, e, reason in ex_good:
                fh.write(f"{n}\t{e}\t{reason}\n")
        print("written")


if __name__ == "__main__":
    main()
