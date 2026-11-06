# Real Exam English Fanwiki – working rules

Language with Alex: German. Everything in the repo, the vault and on the website: English.
Live: https://tscherny86.github.io/realexam/ · Preview artifact: https://claude.ai/artifact/3CwyLUdDPzPmmG15FtFZv5
Obsidian: `Projekte/Real Exam English Fanwiki/` in the repo `tscherny86/notes-vault` (mandatory for every change, see below).
Sister project with the same structure: ABC Podcast Fanwiki (`tscherny86/abcpodcast`).

## Short commands (agreed with Alex for the ABC project on 06.11.2026, apply here too)

Alex only writes the keyword. Do not ask questions – run the whole procedure and report briefly at the end.

### "check" – new episode?
1. Load the feed: `python scripts/check_feed.py`. If buzzsprout is blocked (403), fetch the feed with Firecrawl
   (`firecrawl_scrape`, URL `https://feeds.buzzsprout.com/1107956.rss`, `formats: ["rawHtml"]`, `maxAge: 0`) and run
   `python scripts/check_feed.py --file <saved result>`.
2. If the script reports "no new episodes" (exit 0): answer Alex exactly that – **"keine neuen Episoden"** – done.
3. Otherwise (exit 10) for every reported episode:
   - Find the Spotify episode ID (Spotify MCP search or the show page) and add it to `data/spotify_ids.json`.
   - Transcribe: `python -u scripts/transcribe_local.py <ID>` (GPU, about 15× real time; partial results in
     `data/transcripts/partial/` are resumed after an interruption).
   - Fetch the official transcript: `python scripts/fetch_official.py`.
   - Then **all quality checks as for "quality"** for this episode.

### "quality" – check everything unchecked
Applies to every episode with a transcript that is neither aligned with an official transcript
(`data/alignment_report.json`, `"used": true`) nor listed in `data/proofread.txt`:
1. **Polish the transcript:** read it completely line by line (helpers, 2–3 episodes each), find hearing errors in
   names, places, idioms **and everyday words**. Rules in `data/corrections.tsv` (global only when certain
   everywhere, otherwise local with the episode ID), no smoothing of dialect or grammar. Then add the ID with the
   date to `data/proofread.txt`. Check how many rules fire (`data/corrections_report.json`), fix the ones that don't.
   For aligned episodes only spot-check the alignment ratio (below 0.9 → look at the transcript).
2. **Topic assignment:** check every assignment topic/language/exam/accent of the episode against the quotes:
   real subject or false hit / passing remark? False assignments with a reason in `data/topic_exclusions.tsv`.
   Systematic false hits → sharpen the patterns in `scripts/topics.py` (or raise `min`). Add new topics or
   language points that occur several times.
3. **Build and check:** `python scripts/build_wiki.py`, `python scripts/build_site.py <scratchpad>/site/index.html`,
   look at the pages in the browser (desktop and 390 px) without JS errors and without overflow.
4. **Deliver** (order below), republish the artifact (`build_site.py … --fragment`) and send Alex a table
   **corrections per episode** and the removed assignments.

If nothing is unchecked: answer "alles geprüft, nichts offen".

## Delivery (every change)
1. `package.json` version (patch for corrections/small things, minor for new functions), entry at the top of
   `CHANGELOG.md`, `## Version: X.Y.Z` in the README. Pure transcript commits are content, not a version.
2. Obsidian `Projekte/Real Exam English Fanwiki/`: "Aktuelle Version" in the Steckbrief, entry at the top of the
   Änderungsprotokoll (`## TT.MM.JJJJ – Version X.Y.Z`), Ist-Stand, Chronik, tick off Offene Punkte, for
   corrections also "Transkription und Korrekturen". `git pull --rebase` the vault before pushing (Obsidian Git on
   Alex' PC writes too); no git commands that throw away uncommitted changes. The Obsidian notes are in German.
3. Push to `main`; GitHub Pages builds automatically, `release.yml` creates the release.
4. Projekt-Cockpit: the project is registered in `cockpit.config.ts` (repo `tscherny86/projekt-cockpit`); nothing to
   do there unless repo, live URL or file names change.
