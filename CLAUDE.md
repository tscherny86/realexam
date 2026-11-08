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
Applies to every episode with a transcript that is not listed in `data/proofread.txt` (the official-transcript
alignment does not replace the reading: the official texts contain typos and sometimes lack passages):
1. **Polish the transcript:** `python scripts/qa_scan.py` writes `data/review/scan.md` with suspicious spots per
   episode; then read the transcript completely line by line (helpers, up to 15 episodes each, output as TSV
   `WRONG<TAB>RIGHT<TAB>local<TAB><id><TAB>reason` in `data/review/out/proof-N.tsv`), find hearing errors in names,
   places, idioms **and everyday words**; no smoothing of dialect or grammar. `python scripts/apply_review.py --write`
   validates the rules against the transcripts and appends them to `data/corrections.tsv` (corrections run after the
   alignment, so they also fix the official text). Then add the ID with the date to `data/proofread.txt`. Check
   `data/alignment_report.json`: a large `kept_whisper` value means Whisper passages inside an aligned transcript –
   read those too (they are what `qa_scan` cannot see).
2. **Topic assignment:** `python scripts/review_assignments.py` writes one review file per episode
   (`data/review/assignments/<id>.md`, every assignment with evidence and quotes). Judge every MAIN assignment:
   real subject or false hit / passing remark? Removals as `NAME<TAB><id><TAB>reason` in
   `data/review/out/assign-N.tsv`, merged by `apply_review.py --write` into `data/topic_exclusions.tsv`.
   Systematic false hits → sharpen the patterns in `scripts/topics.py` (or raise `min`); words from Trevor's plugs
   are already ignored (`PLUG` in `build_wiki.py`). Add new topics or language points that occur several times.
3. **Audio marks:** `python scripts/check_marks.py <id>` (GPU) transcribes clips at sample marks and compares them with
   the transcript (`data/review/marks.md`); a mismatch means wrong timestamps or missing text there.
4. **Build and check:** `python scripts/build_wiki.py` (also extracts the vocabulary box, exam questions and
   speakers per episode via `scripts/extract.py`; new noise there → tighten its filters, do not hand-edit the
   vault), `python scripts/build_site.py <scratchpad>/site/index.html`,
   look at the pages in the browser (desktop and 390 px) without JS errors and without overflow.
5. **Deliver** (order below), republish the artifact (`build_site.py … --fragment`) and send Alex a table
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
5. **Pass every update on to Shamrock Script (mandatory, Alex 07.11.2026).** Shamrock Script (Alex' C2 writing
   trainer, a Claude artifact; folder `C:\Users\tsche\OneDrive\ShamrockScript`, repo `tscherny86/shamrock-script`)
   shows this archive as its own "Podcast" menu and must always have the current data. Real Exam stays private and
   is only a data provider for Shamrock Script (decision Alex, 07.11.2026); there is no public site to wait for.
   After **every** commit that changes the site data – a new version *and* pure content commits ("Transcript
   <id>", corrections) – follow **"Podcast data update"** in `ShamrockScript/CLAUDE.md` right away: run
   `python scripts/sync_realexam.py` there (it builds `data.json` locally from this clone with `build_site.py`),
   republish the artifact, commit and push there.
   Only then is the delivery finished; report it to Alex in the same message. If that is impossible in the session,
   say explicitly "Shamrock Script NICHT aktualisiert" – never finish silently. `data.json`/`transcripts.json`
   (format `schema: 1`) may only be extended, never have fields renamed or removed.

## Checks and releases without GitHub (fallback)

Since the GitHub suspension of 07.11.2026 nothing may depend on GitHub alone. The code lives locally, on GitHub and privately on GitLab (`gitlab.com/tschernutter/realexam`); `git push origin` goes to GitLab first.

- **Check:** `python scripts/ci.py` (builds the site into a temp folder, checks articles and version; publishes nothing) – GitLab CI (`.gitlab-ci.yml`, since 08.11.2026 gitlab.com Linux runners instead of acespc) calls the same script.
- **Release:** `node scripts/release.mjs --all-missing --title "Real Exam English Fanwiki"` creates missing tags `vX.Y.Z` and releases with the CHANGELOG section – on GitLab (glab) and, when reachable, on GitHub (gh). `--dry-run` only shows what would happen.
- **Private, never public** (decision Alex 07.11.2026: "real exam bleibt privat und als datenlieferant für shamrock script"). The fanwiki is only a data supplier for Shamrock Script (which has its own login). No public hosting anywhere: no GitLab Pages, no Netlify/Vercel; `pages.yml` (GitHub Pages) stays off (manual only and only with `PAGES_FREIGABE=ja`, which is not set). GitLab CI only builds and checks.
