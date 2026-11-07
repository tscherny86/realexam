# Review batch 1 – systematic problems (s01e01–s03e02, x2020-12-07, x2021-02-19, x2021-06-20)

Counts below are over the 24 transcripts with text in this batch (x2020-12-07 has no assignments).

## 1. Show-notes boilerplate produces "show notes" hits

Every feed description ends with the same credits/ads. They are matched by topic patterns, which turns a
weak transcript signal (≥ 3 mentions) into MAIN:

| Boilerplate in description | Pattern hit | Entry wrongly promoted |
|---|---|---|
| `Music: Wholesome by Kevin MacLeod`, `Ian from the We Dig Music podcast` | `\bmusic\b` | **Music** → MAIN in s02e01 (6 mentions: concert tickets), s03e01 (3 mentions: "music star") – and "show notes" in s02e07 where it happens to be right |
| `For the Real Exam English app` | `\bapps?\b` | **Technology & the Internet** gets a show-notes hit in every episode (s02e09 is genuinely tech, s02e02 only MINOR – luck) |
| `some great language`, `the language used`, `figurative language` | `\blanguages?\b` | **Languages & Language Learning** → MAIN in s02e01, s02e02, s02e05, s02e10 (plus MINOR s02e06) – all meta-talk |
| `For classes - …` | (no pattern yet, but see `\bclass` below) | – |

Suggestion: strip everything from `For classes` / `Music:` / `Thanks to all of the contributors` onwards before
matching the description, or require title/first-sentence hits only.

## 2. Trevor's meta-language and outro boilerplate in the transcript

- **"language"** (43 hits in 18 episodes): "vary your language", "friendship language", "figurative language".
  `\blanguages?\b` should not be a pattern for *Languages & Language Learning*; keep `bilingual`, `mother tongue`,
  `learn(ing) English`, `native speaker`, `fluent`, maybe `foreign language`, `speak \w+ languages`.
- **"examiner(s)"** (55 hits in 18 episodes) makes *Speaking Exam* MAIN almost everywhere, even in s01e08 and the
  writing bonus x2021-02-19 where nothing speaking-specific is said. Explicit `speaking (exam|test|part)` occurs in only
  10 episodes. Either drop `\bexaminer` from the pattern or accept that Speaking Exam is a near-universal tag.
- **Outro ad** "really useful tips on how to prepare for your exam" / "exam preparation classes" (27 hits): the
  `\bprepar(e|ing) for (the|your|an) exam` and `exam (tips?|preparation…)` patterns fire on it in every episode,
  so *Exam Tips & Preparation* is MINOR everywhere and becomes MAIN as soon as a speaker says "nervous"
  (s01e05, s02e09) or Trevor says "revise" (s02e03). `\bnervous\b` is a plain adjective and should go.
- **"Facebook or Instagram"** (38 hits in 18 episodes): `instagram` in *Photography & Photos* produces MINOR in most
  season-1 episodes and MAIN in s01e06 together with a filmmaker's "cameras" and "you can picture it".
- **"students" / "classes" / "course"**: `\bstudents?\b` (22) = exam candidates or Trevor's pupils, `\bclass` (63, mostly
  the classes ad) and `\bcourse` where 30 of 33 hits are "of course". *Learning, School & Education* is MAIN in s01e01,
  s01e10, x2021-06-20 without any education content. Drop `\bcourse` (or use `\bcourses?\b` with a negative lookbehind
  for "of "), drop `\bstudents?\b` or require 2+ other patterns.
- **"Firstly"/"organise"**: `\bfirstly\b` (10) is Trevor's own discourse marker, `organi[sz](e|ing|ation)` (16) matches
  "organizing parties", "organisation", "organise social activities". *Organising Your Answer* → MAIN in s02e01, s02e08
  without any structuring advice. Keep `structure (your|an|the) answer`, `well[- ]structured`, `paragraph plan`.

## 3. Grammar entries matched by ordinary speech, never explained

- *Past Perfect & Narrative Tenses*: `\bused to\b` (35 hits) and `\bwould\b.*\bevery\b` match the speakers' answers;
  explicit tense talk ("past perfect", "past simple" …) occurs once in the whole batch. MAIN in s01e01, s01e04,
  s01e10, s02e01, s02e02 – all false. Drop `used to` and the `would … every` line, keep the explicit names.
- *Modal Verbs*: `\bshould have\b` matches "you should have passive voice, reported speech …" (x2021-02-19).
- *Comparatives & Superlatives*: `\bfar more\b` once in an answer → MAIN (s02e10).
- *Conditionals*: being listed in "mixed conditionals, inverted conditionals" counts as 4 mentions (x2021-02-19).
- *Connectors*: `\bhowever\b`/`\bwhereas\b` are also Trevor's own words; works out acceptably because he usually
  does comment on connectors, but the evidence quotes are then just his narration.
- *Exams · Listening & Reading*: "use of English" fires on the "use of English exercises" ad and on asides
  ("this phrasal verb appears in Use of English a lot") → MAIN in s02e09, s02e10, x2021-06-20.
- *Cambridge C1/C2*: `\bC1\b`, `\bC2\b` fire on level references ("at a C1 level you should know inversions") and on
  the classes ad ("courses for B2, C1 and C2"). I kept them where Trevor repeatedly ties advice to the exam
  (s01e08, s02e03) and removed x2021-06-20 (ad + "my C1 students").

## 4. Topic words used in another sense

| Pattern | False sense | Examples |
|---|---|---|
| `\bspend` (Money) | spend *time* – 19 of 42 hits | s01e05, s02e06, s02e08, s02e09, s02e10 (all MINOR) |
| `\bbuy\b` (Shopping) | "buy yourself time" (fillers), "buy myself beer" | s01e01, s01e08 |
| `\bchang(e…)\b` (Change) | "climate change" | s01e08 |
| `environment` (Environment) | "urban/built-up environment", "work environment" | s02e02, s02e08 |
| `\bextreme` (Extremes) | "extremely", "extreme adjective" | s02e01 |
| `\bthrill` (Extremes) | "thriller" (book genre) | s01e09 |
| `\bscience\b` (Space & Science) | "science fiction" | s01e10 |
| `\bcontent\b` (Happiness) | content of a writing | x2021-02-19 |
| `\bsleep\b` (Health) | "sleep with a teddy bear" | s02e07 |
| `\bhelp(…)\b` (Help & Kindness) | "that always helps", "help me through my twilight years" | s02e08, s02e10 |
| `\bmedia\b` (News & Media) | "social media" (30 of 37 media hits) – already covered by Technology | s01e05 |
| `\bcamera` (Photography) | "security cameras" (city question) | s02e02 |
| `\bfood\b` (Food) | "food shopping", "junk food" as vocabulary | s01e05, s02e04 |
| `\bwork\b` (Work) | "work-life balance", "if you don't work" | s02e05 |
| `\bfriends?\b` (Friends) | friends as companions in another topic ("celebrations with friends", "keep in touch with friends", "funny friends") | s02e01, s02e09, s03e01 |
| `\bparents?\b` (Family) | "parents like their children's friends" | s02e06 |
| `polite`, `\brude` (Manners) | "replace taboo words politely", "disagree politely" – language points | s02e05 |
| `educat` (Learning) | "educational TV" | s01e10 |

*Friends & Friendship* is the judgement call in this list: in s02e09 two exam questions literally contain
"friends" ("How do you keep in touch with friends …?"). I removed it because the discussion is about ways of
communicating, not friendship; if the rule is "question mentions it → MAIN", put s02e09 back.

## 5. Accents – country names as examples, and speakers that are never counted

- *Non-Native Speakers* matches country names (`Spain`, `Italy`, `Vietnam`, `China`, `French`…) that appear as travel
  destinations (s01e02), origins of dishes (s01e03) or a false-friend remark "if you're Spanish" (s01e09). None of
  these episodes has a non-native speaker. The entry needs a different signal (e.g. "non-native", "from Spain/…
  speaking English", speaker label).
- The reverse problem is bigger: accents are usually announced **once** in the intro ("we have people from the
  USA, Australia, Scotland, Ireland and England") and then never named again. With min 2 (MINOR) / 3 (MAIN) these
  speakers are lost. Missing MAIN accents in this batch:
  s02e06 (USA, Australia, Scotland, Ireland), s02e09 (USA, England, Scotland, Australia, Ireland),
  s02e10 (England, USA, Australia), s02e04 (Australia, South Africa), s02e07 (Scotland, Ireland),
  s03e01 (Australia), s02e01 (Scotland – "That, my friends, is a Scottish accent"), s02e02 and s02e03 (England –
  Tamworth/Birmingham and East Midlands speakers), s02e08 (USA – "our first one is from the US"),
  s01e04 and s01e09 (England – speakers labelled "(UK)", but `\bUK\b` is not an England pattern; 14 hits in 7 episodes).
  Suggestions: parse the intro/description sentence "speakers from …" (also "people from", "accents from") and count each
  country named there as MAIN; add `\bUK\b`, `\bBritain\b`, `\bthe North\b`? to England; count speaker labels `Name(Country)`;
  lower the accent threshold to 1 explicit "this speaker is from X".
- s02e05 USA MAIN rests only on "American English expressions / roughhouse is American English" – fine as a discussion of
  US English, but the actual speakers' origins are unknown.

## 6. Thresholds

- Topics FOLDER_MIN 10 works for the title topic but a side topic with 10–15 generic hits (`work`, `money`, `friends`,
  `parents`) is usually noise; genuine side subjects in this batch (Money in s01e04/s02e04/s02e05, Transport in s02e02,
  Art in s02e07, News in s02e03/s02e09, Fashion in s02e04, TV in s03e01, Parenting in s02e10) are backed by an actual exam
  question. A rule "side topic needs ≥ 10 hits **and** a question line containing the pattern" would remove most false MAINs.
- Language/Exams min 3 is too low when the pattern includes everyday words (`used to`, `should have`, `far more`, `however`,
  `nervous`, `examiner`). Entries whose patterns are explicit names only (`phrasal verb`, `cleft`, `inversion`, `question tag`,
  `passive`) are reliable at 3.
- "show notes + 3 mentions → MAIN" is the main source of false MAINs because of the boilerplate (section 1); after cleaning the
  description it is a good rule.

## 7. Things discussed in several episodes that have no entry

- **British vs American English** (s01e08 aluminium/aluminum, consistency advice; s02e01 fancy dress/costume party;
  s02e04 shopping centre/mall, "a girlfriend"; s02e05 roughhouse/horseplay; s01e05 crisps/potato chips; s01e03 take out/take away).
- **Expressing likes, dislikes and preferences** (s01e06 "I can't stand / I'm fond of / I adore", s02e04 "I'd rather / I prefer",
  s02e07 "avid / voraciously") – Trevor presents it as a named skill.
- **Buying time / fillers** ("well…", "that's an interesting question", "gosh", "off the top of my head") – s01e01, s01e03, s01e05.
- **Dialogue / interaction skills** (agreeing, disagreeing, interrupting politely, not agreeing too soon, Cambridge part 3 format) –
  s02e02, s02e04, s02e06, x2021-06-20; currently only indirectly under *Speaking Exam*.
- **Speculating / hedging language** (s02e02 "perhaps, I think they tend to, a good deal faster", later photo-speculation episodes).
- **Intensifiers and extreme adjectives** (s02e01 "remarkably, extremely, awesome"; s02e02 "a good deal faster"; s01e04 "not nearly as good as").
- **Synonyms / avoiding basic words** (s01e09 seven ways to say "important"; s02e10 "big, good, bad don't impress"; s03e01 "7 ways to say the same thing").
- **Participle clauses** (s02e03, x2021-02-19 – named alongside cleft sentences and inversions).
- **Covid / lockdown** as a recurring discussion subject in season 2 (s02e01, s02e05, s02e07, s02e09, s02e10) – no topic entry.
- **Compound nouns** are only covered via *Adjectives & Compound Adjectives*; fine, but the summary could say so.
- s01e03: South Africa speaker (Mary) is labelled "(South Africa)" but Trevor says she lives in Ireland – South Africa is not
  assigned at all; not a pattern problem, just worth knowing.
