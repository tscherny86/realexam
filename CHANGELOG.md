# Changelog – Real Exam English Fanwiki

Newest version on top. Every delivered version gets an entry here and a GitHub release with the tag `vX.Y.Z`
(created automatically by `.github/workflows/release.yml`). Times are CET.
New transcripts (commits "Transcript <id>") are content, not a version of their own.

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
