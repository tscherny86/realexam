#!/usr/bin/env python3
"""Builds the website (one single HTML file) from the Obsidian vault.

Usage:
    python scripts/build_site.py                       # -> _site/index.html (for GitHub Pages)
    python scripts/build_site.py out.html --fragment   # without the <html> skeleton (preview artifact)

The vault (Real-Exam-English-Wiki/) stays the source. This script reads the notes, turns them into
structured data (episodes, articles, quotes, transcripts) and inserts them into site/template.html.
It runs on every push through the GitHub Action.
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "Real-Exam-English-Wiki"
TEMPLATE = ROOT / "site" / "template.html"
HOME = "Real Exam English Wiki"
KIND = {"Topics": "topic", "Language": "language", "Exams": "exam", "Accents": "accent"}
_PR = ROOT / "data" / "proofread.txt"
PROOFREAD = {l.split("\t")[0].strip() for l in (_PR.read_text(encoding="utf-8").splitlines() if _PR.exists() else []) if l.strip() and not l.startswith("#")}

WIKI = re.compile(r"\[\[([^\]]+?)\]\]")
MDLINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def slugify(s: str) -> str:
    s = s.replace("&", " and ")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def split_fm(md: str):
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if not m:
        return {}, md
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, md[m.end():]


def sections(body: str):
    """'## Title' -> content"""
    out, cur, buf = {}, "_intro", []
    for line in body.split("\n"):
        if line.startswith("## "):
            out[cur] = "\n".join(buf).strip()
            cur, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out[cur] = "\n".join(buf).strip()
    return out


def label_to_sec(t: str) -> int:
    p = [int(x) for x in t.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


class Site:
    def __init__(self):
        self.notes = {}  # name -> (folder, frontmatter, body)
        for p in sorted(VAULT.rglob("*.md")):
            rel = p.relative_to(VAULT)
            folder = rel.parts[0] if len(rel.parts) > 1 else ""
            fm, body = split_fm(p.read_text(encoding="utf-8"))
            self.notes[p.stem] = (folder, fm, body)
        self.route = {}
        for name, (folder, fm, _) in self.notes.items():
            if folder == "Episodes":
                self.route[name.lower()] = "episode-" + name.split()[0]
            elif folder == "Transcripts":
                self.route[name.lower()] = "transcript-" + name.split()[-1]
            elif folder in KIND:
                self.route[name.lower()] = f"{KIND[folder]}-{slugify(name)}"
        self.route.update({HOME.lower(): "home", "all episodes": "episodes", "topics": "topics",
                           "language": "language", "exams": "exams", "accents": "accents"})

    # ---------- links & small markdown ----------
    def wiki_target(self, inner: str):
        inner = inner.replace("\\|", "|")
        target, _, alias = inner.partition("|")
        name, _, anchor = target.partition("#")
        r = self.route.get(name.strip().lower())
        if r and anchor.startswith("Minute "):
            r += "-m" + anchor.split()[-1]
        return r, (alias or name).strip()

    def inline(self, s: str) -> str:
        tokens = []

        def keep(h):
            tokens.append(h)
            return f"\x00{len(tokens) - 1}\x00"

        def wl(m):
            r, text = self.wiki_target(m.group(1))
            return keep(f'<a href="#{r}">{html.escape(text)}</a>' if r else html.escape(text))

        s = WIKI.sub(wl, s)
        s = MDLINK.sub(lambda m: keep(f'<a href="{html.escape(m.group(2))}" target="_blank" rel="noopener">'
                                      f'{html.escape(m.group(1))}</a>'), s)
        s = html.escape(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", s)
        s = re.sub(r"(?<![\w*])_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<em>\1</em>", s)
        return re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m.group(1))], s)

    def blocks(self, md: str) -> str:
        """Paragraphs, lists, quotes. Obsidian callouts are left out."""
        out, para, items, quote = [], [], [], []

        def flush():
            if para:
                out.append("<p>" + self.inline(" ".join(para)) + "</p>")
                para.clear()
            if items:
                out.append("<ul>" + "".join(f"<li>{self.inline(i)}</li>" for i in items) + "</ul>")
                items.clear()
            if quote:
                if not quote[0].startswith("[!"):
                    out.append("<blockquote><p>" + self.inline(" ".join(quote)) + "</p></blockquote>")
                quote.clear()

        for line in md.split("\n"):
            s = line.strip()
            if not s or s in {"_", "---"}:
                flush()
            elif s.startswith(">"):
                if para or items:
                    flush()
                quote.append(s.lstrip(">").strip())
            elif re.match(r"^[-*] ", s):
                if para or quote:
                    flush()
                items.append(s[2:])
            elif items and line.startswith("  "):
                items[-1] += " " + s
            else:
                if items or quote:
                    flush()
                para.append(s)
        flush()
        return "".join(out)

    # ---------- content ----------
    def episodes(self):
        eps = []
        for name, (folder, fm, body) in self.notes.items():
            if folder != "Episodes":
                continue
            sec = sections(body)
            h1 = re.search(r"^# (.+)$", body, re.M).group(1)
            title = re.sub(r"^S\d+\s*-\s*\d+\s*", "", h1).strip() or h1
            mp3 = re.search(r"\[MP3\]\((\S+?)\)", body)

            def row_links(label):
                out = []
                row = re.search(rf"^\| \*\*{label}\*\* \| (.*) \|$", body, re.M)
                for m in WIKI.finditer(row.group(1) if row else ""):
                    r, text = self.wiki_target(m.group(1))
                    if r:
                        out.append([r, text])
                return out

            topics = [t for lab in KIND for t in row_links(lab)]
            minor = row_links("Briefly mentioned")
            speakers = row_links("Speakers from")
            marks = []
            for line in sec.get("Chapters", "").splitlines():
                m = re.match(r"- \[(\d+:\d{2})\]\(\S+?\) – (.*?) \(\[\[", line)
                if m:
                    marks.append([label_to_sec(m.group(1)), m.group(2)])
            vocab = [[m.group(1), m.group(2), label_to_sec(m.group(3))] for m in re.finditer(
                r"^- \*\*(.+?)\*\* \((.+?)\) – \[(\d+:\d{2})\]\(", sec.get("Language from this episode", ""), re.M)]
            qs = [[m.group(2), label_to_sec(m.group(1))] for m in re.finditer(
                r"^- \[(\d+:\d{2})\]\(\S+?\) (.+?)$", sec.get("Exam questions", ""), re.M)]
            spotify = fm.get("spotify", "")
            ep_id = name.split()[0]
            tx_status = re.search(r"\| \*\*Transcript\*\* \| \[\[Transcript [^\]]+\]\] \([^,]+, (.*?)\)", body)
            eps.append({
                "id": ep_id, "label": fm.get("label", ""), "kind": fm.get("kind", "episode"),
                "season": int(fm.get("season", 0)), "num": int(fm.get("number", 0)),
                "title": title, "year": int(fm.get("year", 0)), "date": fm.get("date", ""),
                "dur": fm.get("duration", ""), "spotify": spotify if "/episode/" in spotify else "",
                "mp3": mp3.group(1) if mp3 else "", "tx": fm.get("transcript") == "true",
                "status": (tx_status.group(1).replace("*", "") if tx_status else ""),
                "topics": topics, "minor": minor, "notes": self.blocks(sec.get("Show notes", "")), "marks": marks,
                "speakers": speakers, "vocab": vocab, "qs": qs,
            })
        eps.sort(key=lambda e: (e["date"], e["id"]), reverse=True)
        return eps

    def entries(self):
        out = []
        for name, (folder, fm, body) in self.notes.items():
            if folder not in KIND:
                continue
            sec = sections(body)
            lead = re.search(r"^_(.+)_$", sec["_intro"], re.M)
            quotes = []
            for block in re.split(r"\n\s*\n", sec.get("Said in the podcast", "")):
                lines = [l[1:].strip() for l in block.splitlines() if l.startswith(">")]
                text = " ".join(l for l in lines if l and not l.startswith("—"))
                src = next((l for l in lines if l.startswith("—")), "")
                ep = re.search(r"\[\[([a-z0-9-]+) ", src)
                tm = re.search(r"\[Minute (\d+:\d{2})\]", src)
                if text and ep and tm:
                    quotes.append([ep.group(1), label_to_sec(tm.group(1)), text.strip("… ").strip()])

            def ep_lines(prefix):
                out = []
                key = next((k for k in sec if k.startswith(prefix)), None)
                for line in (sec.get(key, "") if key else "").splitlines():
                    m = re.match(r"- \[\[([a-z0-9-]+) ", line)
                    if m:
                        times = [label_to_sec(t) for t in re.findall(r"\[(\d+:\d{2})\]\(", line)]
                        out.append([m.group(1), "Show notes" in line, times])
                return out

            eps, minor = ep_lines("In these episodes"), ep_lines("Briefly mentioned")
            out.append({
                "r": self.route[name.lower()], "name": name, "kind": KIND[folder],
                "lead": lead.group(1) if lead else "",
                "count": len(eps),
                "expl": self.blocks(sec.get("Background", "")), "quotes": quotes, "eps": eps, "minor": minor,
                "level": [x.strip() for x in fm.get("level", "").strip("[]").split(",") if x.strip()],
                "exams": [x.strip() for x in fm.get("exams", "").strip("[]").split(",") if x.strip()],
            })
        out.sort(key=lambda e: e["name"].lower())
        return out

    def transcripts(self):
        tx = {}
        for name, (folder, fm, body) in self.notes.items():
            if folder != "Transcripts":
                continue
            rows = [[label_to_sec(m.group(1)), m.group(2).strip()] for m in re.finditer(
                r"^### Minute \d+\n\[▶ (\d+:\d{2})\]\(\S+\)\s*\n(.*?)(?=\n### |\Z)", body, re.S | re.M)]
            tx[name.split()[-1]] = rows
        return tx

    def hours(self):
        h = re.search(r"\*\*(\d+) h (\d+) min\*\*", self.notes[HOME][2])
        return [int(h.group(1)), int(h.group(2))] if h else [0, 0]


CSP = ("default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; img-src data:; media-src https:; connect-src 'none'; "
       "base-uri 'none'; form-action 'none'; object-src 'none'")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fragment = "--fragment" in sys.argv
    out = Path(args[0]) if args else ROOT / "_site" / "index.html"
    site = Site()
    eps = site.episodes()
    data = {"eps": eps, "entries": site.entries(), "tx": site.transcripts(), "hours": site.hours()}
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    version = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
    page = TEMPLATE.read_text(encoding="utf-8").replace("__VERSION__", version).replace("__DATA__", payload)
    if not fragment:
        page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                # Security headers: GitHub Pages allows no custom HTTP headers, so these go in as meta tags
                # as far as browsers support them (CSP without frame-ancestors, Referrer-Policy).
                f'<meta http-equiv="Content-Security-Policy" content="{CSP}">\n'
                '<meta name="referrer" content="strict-origin-when-cross-origin">\n'
                '<meta name="description" content="Real Exam English Fanwiki – B2, C1, C2. '
                'Every topic, idiom and grammar point linked to the episode and the exact minute.">\n' + page + "\n</html>\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    if not fragment:
        (out.parent / ".nojekyll").touch()
    print(f"{len(eps)} episodes, {len(data['entries'])} entries, {len(data['tx'])} transcripts -> {out} "
          f"({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
