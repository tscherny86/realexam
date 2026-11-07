# Changelog – Real Exam English Fanwiki

Newest version on top. Every delivered version gets an entry here and a GitHub release with the tag `vX.Y.Z`
(created automatically by `.github/workflows/release.yml`). Times are CET.
New transcripts (commits "Transcript <id>") are content, not a version of their own.

## Unreleased

- Operations (07.11.2026, GitHub suspension): `scripts/ci.py` and `scripts/release.mjs`; `release.yml` and the new `.gitlab-ci.yml` (runner acespc) only call these scripts. `pages.yml` no longer runs on push, only manually with `PAGES_FREIGABE=ja` (publishing blocked until Alex decides). No new version, the site is unchanged.

## 1.4.0 – 07.11.2026
- **Open data for other apps.** Every site build now also writes `data.json` (episodes with vocabulary box, exam
  questions and minute marks; all entries with quotes, level and exams) and `transcripts.json` (all transcripts,
  minute by minute) next to the page: https://tscherny86.github.io/realexam/data.json and `…/transcripts.json`.
  Format `schema: 1` with `version` and `built` (UTC) on top, the same content the page itself uses. The first
  reader is Shamrock Script (Alex' C2 writing trainer), which shows the archive as its own "Podcast" menu; the
  fanwiki itself does not change and keeps running on its own.

## 1.3.0 – 07.11.2026
- **Four expansions of the site** (Alex: "Ausbaustufen einbauen"), all generated from the transcripts by the new
  `scripts/extract.py`:
  - **Language from this episode:** the expressions Trevor picks out by name ("the phrasal verb to put off means…",
    "we had the expression a blast from the past") as a box on every episode page, each with the minute it is
    explained at – 117 expressions in 56 episodes. Deliberately strict: only what is named as a phrasal verb,
    idiom, expression, collocation or explained word counts, so the box stays clean.
  - **Exam questions:** the questions Trevor asks the native speakers (453 in 68 episodes), listed on the episode
    page with the minute the answers start, plus a new **Practice** page with a random question ("Another
    question"), the full question bank with a filter, and the same questions in the search. The home page shows
    one random question too.
  - **Speakers from:** the accents Trevor announces in the intro (first two minutes) or the show notes as a line
    of their own on the episode page (48 episodes) – different from the Accents tags, which also cover accents
    that are only talked about.
  - **Level and exam filter:** every topic, language point and exam is rated B2/C1/C2 and Cambridge/IELTS
    (`LEVELS` and `EXAMS` in `scripts/topics.py`); the Topics, Language and Exams pages filter by level (Exams also
    by exam), the tiles and article pages show the level badges.
- Mobile navigation holds the seventh item (narrower spacing, scrolls if a phone is narrower than 375 px).

## 1.2.0 – 07.11.2026
- **Four new topics** that the reviewers' counts showed to carry real weight across the episodes: **Nature &
  Outdoors** (9 episodes), **Social Media** (8, taken out of Technology & the Internet), **Politics & Government** (5)
  and **Age & Generations** (6). Now 110 articles: 57 topics, 34 language points, 9 exams, 10 accents.
- Reviewer suggestions that are too rare for an article of their own went into existing ones as paragraphs:
  gun control and racism (Crime & Law), participle clauses (Relative Clauses), rhetorical questions and the sandwich
  technique (Organising Your Answer), connected speech (Pronunciation), dialogue and interaction skills (Speaking
  Exam), synonyms for basic words (Adjectives), paraphrasing (Writing Exam).

## 1.1.0 – 07.11.2026
- **Full quality pass over all 75 transcripts** (Alex: "der DICKE Qualitätscheck"). Five helpers read every transcript
  line by line: 197 new rules in `data/corrections.tsv`, 205 corrections in 60 episodes (misheard names and
  idioms such as "Queen Bee" → "Queanbeyan", "part run" → "parkrun", "repel" → "rappel", "Santa Paula" → "Santa Pola",
  typos and wrong apostrophes in the official transcripts, glued sentence boundaries). Corrections now run **after**
  the alignment, so they also fix the official text. Every episode is listed in `data/proofread.txt`.
- **Alignment with the official transcripts made safe.** Passages that the official text has elsewhere or not at all
  were squeezed into one word and content went missing (S1 E2 minutes 4–7, S1 E9 minute 3, S2 E6 duplicate answer).
  Unequal blocks now keep the Whisper words (`kept_whisper` in `data/alignment_report.json`); those passages were
  proofread separately. Acute accents from a Spanish keyboard (`´`) in the official text become apostrophes.
- **Topic assignment reviewed for every episode.** Three helpers judged all 1,259 assignments against the quotes:
  186 removed (`data/topic_exclusions.tsv`). Systematic causes fixed in `scripts/topics.py` and `build_wiki.py`:
  Trevor's recurring plugs (website, classes, Facebook/Instagram, app, coffee) and the show-notes credits ("Thanks to
  all of the contributors", "We Dig Music podcast", "Music: Wholesome by Kevin MacLeod") no longer count; grammar
  points only count when Trevor actually names them (no more "used to", "however", "not only", "interested in" from
  natural speech); "of course", "spend time", "law professor", "climate change" → Change, "IELTS band" → Music, country
  names as examples → Non-Native Speakers and similar false senses removed; language points, exams and accents
  announced in the show notes or in Trevor's intro count straight away. New entries: Drugs & Legalisation,
  Globalisation, Covid & Lockdown, Buying Time & Fillers, Substitution & Ellipsis, Gerund or Infinitive,
  Intensifiers, British vs American English, Likes, Dislikes & Preferences, Speculating & Hedging (106 articles).
  Result: on average 6.8 main tags per episode, all backed by the transcript.
- **Audio marks tested against the audio.** `scripts/check_marks.py` cuts 8 seconds at a sample of minute marks,
  transcribes the clip and compares it with the transcript: 296 samples over all episodes, 5 mismatches (all
  explained by the alignment gaps above); after the fix 100 further samples on the affected episodes, 0 mismatches.
  Player checked on the live site (click at 4:24 plays from 4:24).
- **New quality tools** for the "quality" command: `qa_scan.py` (flags odd tokens and rare words),
  `review_assignments.py` (one review file per episode with the evidence), `check_marks.py`, `apply_review.py`
  (merges helpers' findings after validating them against the transcripts).
- Transcript page: a minute link whose exact row does not exist now jumps to the nearest earlier row.

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
