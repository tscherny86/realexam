# Changelog – Real Exam English Fanwiki

Newest version on top. Every delivered version gets an entry here and a GitHub release with the tag `vX.Y.Z`
(created automatically by `.github/workflows/release.yml`). Times are CET.
New transcripts (commits "Transcript <id>") are content, not a version of their own.

## 1.0.0 – 07.11.2026
- **All 75 episodes transcribed** overnight on the GPU (faster-whisper `large-v3-turbo`, about 15× real time); 68 of them
  merged with the official Buzzsprout transcript (word match 96–98 %, `data/alignment_report.json`), the 7 episodes
  without one (S1 E1, E5, E8, E10, S4 E5, the trailer and the app announcement) proofread by hand with the correction
  list (`data/corrections.tsv`, e.g. "Joe Blocks" → "Joe Bloggs", "emailed for the future" → "earmarked for the future").
- **Topic assignment recalibrated** (Alex: assignments must "really make sense"). With the ABC rule (3 mentions) every
  episode carried 10–20 main topics, because the speakers roam through many subjects in one answer. Measured on the
  first 23 transcripts: the episode's real subject is named 30–70 times, genuine side subjects 10–25, noise up to 8.
  Now: Topics need 10 mentions (briefly mentioned from 4), Language/Exams/Accents 3 (from 2); show-notes hits only
  count with at least 3 mentions in the transcript, title hits always. Result: 3–6 main topics per episode.
- **All 75 Spotify episode IDs** mapped, so "Spotify ↗" jumps to the exact minute everywhere.
- Whisper fragments glued back together ("high -level" → "high-level", "studio .com" → "studio.com", "20 %" → "20%").
- Writing-exam patterns no longer fire on everyday "review", "report" or "article".
- Preview artifact published; Obsidian project folder and Projekt-Cockpit entry (0.8.4) complete.

## 0.1.0 – 06.11.2026
- **First version**, built to the same blueprint as the ABC Podcast Fanwiki: Obsidian vault with all 75 episodes
  from the RSS feed (seasons 1–6 plus bonus episodes, 2020–2026), articles for 50 topics, 27 language points,
  9 exams & skills and 10 accents, each with background knowledge, quotes and links to the exact minute
  (Spotify `?t=`), transcript pipeline, single-page website with its own player and full-text search.
- **Transcription on the GPU:** faster-whisper `large-v3-turbo` on Alex' RTX 3070 (about 15× real time), word
  timestamps, resumable. **Official transcripts** from Buzzsprout (68 of 75 episodes) are downloaded and merged
  with the Whisper timestamps (`align_official.py`), so those transcripts carry the official wording.
- **Topic assignment** as in the ABC project: main topic from a title/show-notes hit or at least 5 mentions,
  otherwise "briefly mentioned"; hand-checked exclusions in `data/topic_exclusions.tsv`; correction list
  `data/corrections.tsv` for the episodes without an official transcript.
- **Design** follows the podcast artwork: deep green, black disc logo, white condensed type; light and dark mode;
  episode badges "S6 · E10"; everything on the site in English.
- GitHub Pages workflow, release workflow, versioning (`package.json`, this changelog, README), Obsidian project
  folder `Projekte/Real Exam English Fanwiki/` and entry in the Projekt-Cockpit.
