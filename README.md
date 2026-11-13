# Real Exam English Fanwiki 🎧

## Version: 1.4.2

Repo: https://gitlab.com/tschernutter/realexam (private) · Changes: [CHANGELOG.md](CHANGELOG.md) · Releases: https://gitlab.com/tschernutter/realexam/-/releases

No public site: the content appears in the "Podcast" menu of Shamrock Script.

**State of 1.3.0:** all 75 episodes with transcripts (68 aligned with the official Buzzsprout transcript, all 75 proofread by hand, 205 corrections), 110 articles (57 topics, 34 language points, 9 exams, 10 accents) rated by level (B2/C1/C2) and exam, every topic assignment reviewed (186 removed), audio marks verified against the audio, all Spotify episode IDs mapped; per episode the expressions Trevor picks out by name (117) and the exam questions he asks (453, also as a practice page with a random question), plus the speakers' origins from the intro.

Fanwiki for the [Real Exam English podcast](https://open.spotify.com/show/0aJJIQVuhGJcM7S2TJIjrW)
(B2, C1, C2) by Trevor – native speakers answer exam-style questions, Trevor picks out the best
language. Built as an **Obsidian vault** plus a single-page website.

## Open in Obsidian (on a PC)
1. Download the repo on GitLab: **Code → Download source code → zip** (or `git clone`) and unzip it,
   e.g. to `Documents/RealExam`.
2. Open Obsidian → **"Open folder as vault"** → choose the folder `Real-Exam-English-Wiki`.
3. Start page: **Real Exam English Wiki**.

## Contents
- `Real-Exam-English-Wiki/Episodes/` – all 75 episodes (2020–2026) with show notes, duration, Spotify and MP3 link,
  where the speakers come from, the expressions Trevor picks out ("Language from this episode") and the exam
  questions he asks, each with its minute
- `Real-Exam-English-Wiki/Topics/`, `Language/`, `Exams/`, `Accents/` – wiki articles with background
  knowledge + the list of episodes; for transcribed episodes with quotes and a link to the **exact minute**
  (Spotify `?t=seconds`)
- `Real-Exam-English-Wiki/Transcripts/` – word-level transcripts, linked minute by minute

## Update
```bash
python scripts/check_feed.py            # new episodes in the feed?
pip install faster-whisper
python scripts/transcribe_local.py      # transcribe missing episodes on your PC (free, GPU if available)
python scripts/fetch_official.py        # official Buzzsprout transcripts (merged with the timestamps)
python scripts/build_wiki.py            # rebuild the vault (from data/)
```
New topics or language points: `scripts/topics.py`.

## Data
- `data/feed.xml` – RSS feed (https://feeds.buzzsprout.com/1107956.rss, state 06.11.2026, 75 episodes)
- `data/spotify_ids.json` – Spotify episode IDs (for minute links)
- `data/transcripts/` – raw Whisper transcripts with word timestamps
- `data/official/` – official Buzzsprout transcripts (text only); `data/alignment_report.json` shows how well they matched
- `data/corrections.tsv` – correction list for hearing errors, report per episode in `data/corrections_report.json`
- `data/topic_exclusions.tsv` – hand-checked false topic assignments
- `data/proofread.txt` – episodes proofread by hand (those without an official transcript)

## Website and open data

`scripts/build_site.py` turns the vault into a single page (`site/template.html` is the template).
The page is not published; GitLab CI only builds it to check it.
Since 1.4.0 it also writes `data.json` and `transcripts.json` (format `schema: 1`, with `version` and `built`) for
other apps; Shamrock Script reads them. Keep the format backwards compatible: add fields, never rename or remove.
Test locally: `python scripts/build_site.py` → open `_site/index.html` in the browser.

## Versioning
Version in `package.json`, entry at the top of `CHANGELOG.md`, heading `## Version` here in the README.
On push to `main` GitLab CI (`scripts/release.mjs`) creates the GitLab release `vX.Y.Z`. Documentation in Obsidian:
`Projekte/Real Exam English Fanwiki/` (repo `tschernutter/notes-vault` on GitLab).

## Checks and releases

The code lives privately on GitLab (`gitlab.com/tschernutter/realexam`): remote `origin`, branch `main`.

- **Check:** `python scripts/ci.py` (builds the site into a temp folder, checks articles and version; publishes nothing) – GitLab CI (`.gitlab-ci.yml`, gitlab.com Linux runners) calls the same script.
- **Release:** `node scripts/release.mjs --all-missing --title "Real Exam English Fanwiki"` creates missing tags `vX.Y.Z` and GitLab releases with the CHANGELOG section (glab on the PC, GitLab API in CI). `--dry-run` only shows what would happen.
- **Private, never public** (decision Alex 07.11.2026: "real exam bleibt privat und als datenlieferant für shamrock script"). The fanwiki is only a data supplier for Shamrock Script (which has its own login). No public hosting anywhere: no GitLab Pages, no Netlify/Vercel. GitLab CI only builds, checks and creates releases.
