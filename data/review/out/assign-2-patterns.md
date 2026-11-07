# Assignment review 2 – systematic problems

Episodes: s03e03–s03e10, x2022-07-16, x2022-10-14, x2023-01-27, s04e01–s04e10, x2024-04-16, x2024-05-01, x2024-06-29, x2024-08-02 (25). Patterns refer to `scripts/topics.py`.

## 1. Show notes: the credits paragraph produces false "show notes" hits

The "Thanks to all of the contributors…" paragraph is matched like real show notes:

- **Music** ← "Ian from the *We Dig Music* podcast" (all s03 episodes; MAIN in s03e08 and x2022-10-14 although music is only a passing example).
- **Travel, Holidays & Tourism** ← "Leanne from the *Beach Travel Wine* podcast" (all s04 episodes; MAIN in s04e01 Crime, s04e04 Weather, s04e06 Transport, s04e10 Future).

Fix: cut the show notes at "Thanks to" / "Thanks to all of the contributors" before matching. The same paragraph also feeds Non-Native Speakers (none here, but "Loli" etc. are harmless).

## 2. Search words that hit another sense

| Entry | Pattern | False sense | Examples |
|---|---|---|---|
| Learning, School & Education | `\bcourse` | "of course" | s04e01 MAIN with 15 hits ("the US of course", "Well of course"); s04e06 MINOR ("of course, the tube") |
| Languages & Language Learning | `\blanguages?\b` | "language" = vocabulary in Trevor's commentary | s03e03 "cool new language", s03e05/s03e06 "brilliant language", s04e09 "super fancy language", s03e10 "super language" → MAIN in s03e05, s03e06, s04e09 |
| Money & Finance | `\bspend` | "spend time" | x2024-08-02 show notes "spending some time in an English speaking country" → MAIN; s04e03 "spend most of my time" |
| Money & Finance | `\bexpensive\b`, `\bbuy\b` | ordinary adjective / Trevor's "buy me a coffee" plug | s04e03, s03e04 |
| Shopping & Consumerism | `\bbuy\b`, `\bbought\b`, `\bbrands?\b` | "money can't buy happiness", "what would you buy if you had a lot of money", "buy me a coffee" (donation plug in every episode), "brand-new topic" | s03e04 MAIN, s03e03 |
| Crime & Law | `\blaws?\b` | law as profession/subject | x2024-08-02 "law professor", "law school", "international law" → MAIN |
| Communication | `\bchat\b`, `communicat` | "we have a chat with…" (intro of every interview episode), "excellent communicator", "communication marks" (Trevor's assessment), "chat GPT" | x2024-06-29, x2024-08-02 MAIN; s04e10 |
| Work & Careers | `\bwork\b`, `\bjobs?\b` | "hard work raising kids", "the buses work", "our job is to help them", "pretty damn good job" | s04e07 MAIN, s04e04 |
| Anger & Emotions | `\bfeelings?\b`, `emotion` | collocations in photo description ("evoke strong feelings", "trigger emotional feelings") | s03e03 MAIN |
| Happiness | `\bhappy\b` | "looks happy" in photo description; Trevor's "I'd be happy to help / happy to respond" (class ad in most episodes); "as happy as Larry" | s03e05 MAIN; s03e04, s03e10, x2022-10-14 |
| Food & Cooking | `\bfood\b` | "their food or their music" as examples in the question | s03e09 MAIN |
| Sport & Exercise | `exercis` | "use of English exercise", "grammar and vocabulary exercises" | s03e08, s04e02 MINOR |
| Health & Wellbeing | `\bsleep\b` | "sleep on floors" (backpacking) | s04e08 |
| Extremes & Adventure | `\bextreme` | "extremely expensive/effective" | s03e04, s04e04 |
| Help & Kindness | `\bhelp(ing|ed|s)?\b` | Trevor's class ad "if you need any help preparing for an exam", "help you improve" – in almost every episode | s03e07, s03e08, s04e02, s04e07 (all MINOR, harmless but noise) |
| Music | `\bband\b` | IELTS "Band 7 / Band 8" | x2024-06-29 MINOR |
| TV, Film & Entertainment | `\bfilms?\b` | photographic film ("get your film developed") | s03e03 |
| Parenting & Children | `\bchild\b`, `\bchildren\b` | child as learner age ("easier when you're a child") | s04e02 MAIN |
| Family & Relationships / Parenting & Children | `\bparents?\b` in both | one pocket-money question gives two MAIN tags | s03e04 |
| Organising Your Answer | `organi[sz](e|ing|ation)` | "neighborhood organization", "grassroots organisations", "package tours … everything is organised for you" | s03e10 (MAIN justified by other content, evidence wrong), s04e08 |

## 3. Language points assigned on speakers' natural usage, without Trevor explaining anything

These patterns match the *use* of a structure, not its *explanation*, so the Language tag becomes MAIN although it is not a feature of the episode:

- **Prepositions** `\binterested in\b` → MAIN in s03e06, s03e09, s04e09 purely from "interested in fashion/culture/history". Drop this pattern (and `depend on`) or let it count only as MINOR.
- **Inversion** `\bnot only\b` → "not only X but also Y" without inversion (x2024-04-16, x2024-08-02 MAIN). Better: `not only (do|does|did|is|are|was|were|have|has|had|can|could|will|would|should)\b` plus `inversion|inverted`.
- **Modal Verbs** `\bmight have\b`, `\bshould have\b` → ordinary "we might have a different…" (s03e10 MAIN).
- **Connectors & Linking Words** `\bhowever\b`, `\bwhereas\b` → every speaker says "however" (s03e03, s04e02 MAIN). Keep the lexical words only as MINOR evidence; MAIN should need `connector|linking word|linker|discourse marker|cohesi`.
- **Past Perfect & Narrative Tenses** `\bused to\b` → "to be used to doing" (an error Trevor explains in x2024-04-16), "that's what I'm used to" (s04e03).
- **Writing Exam** `\bessays?\b` → anecdote "learn off a full essay" at school (s04e02 MAIN); also Trevor's throwaway "you couldn't use it in an essay".
- **Slang & Informal English** `\bgonna\b` → 15 speaker "gonna"s make x2024-08-02 MAIN (kept only because Trevor also discusses "like" and "hold my beer"); show notes "you're gonna hear" (s04e04).
- **Common Mistakes** `\bmistakes?\b` → in s03e05 and s04e02 the *topic* of the question is "learning by making mistakes"; kept, but the pattern should rather be `common (mistakes?|errors?)|an? (common|typical|little) error|I (often|sometimes) hear`.
- **Pronunciation** `pronounc` → speakers talking about pronunciation as a learner problem (s04e02 MAIN) vs. Trevor explaining a word (s04e03, s04e06 – correct).

## 4. Exams

- **Speaking Exam** `\bexaminer` hits Trevor's "that would impress the examiner" in practically every episode, so the tag is MAIN wherever three such remarks occur (s03e08) and absent elsewhere. Either make it a default tag or require a concrete skill: `speculat(e|ing|ion)`, `describ(e|ing) (a |the )?(photo|picture)`, `long turn`, `monologue`, `discourse management`, `interactive communication`, `time-buy|buy (yourself )?(some|a bit of) time|stalling`, `sandwich technique`, `interlocutor`.
- **Cambridge C2 Proficiency** `\bC2\b` → "a C2 idiom", "C2 level in the Cambridge dictionary", "difference between C1 and C2" (s04e06 MAIN). MAIN should need `C2 exam|C2 Proficiency|CPE|Proficiency`.
- **x2024-05-01 (monologue on legalising marijuana) has no Exams tag** although it is a model Speaking-exam monologue: add `monologue` to Speaking Exam.

## 5. Accents

- **Non-Native Speakers** via `\bSpain\b|\bSpanish\b|\bItalian\b|\bFrench\b|\bGerman\b`: Trevor lives and teaches in Spain, so "here in Spain", "my students from Spain and Italy", "Spanish and Italian speakers often say…", "comes from French", "a German archaeologist" occur constantly → false MAIN in s03e09, s03e10, s04e04, s04e07, s04e08, s04e09 (six of my 25 episodes). Native speakers *living* in Spain (s03e09 linguistics professor, s03e10 Seville speaker, s04e04 UK speakers) are also caught. Suggest: country names count only as MINOR; MAIN only via title/show notes ("from Spain", "non-native", "Martyna from Poland") or `non-native speaker`.
- **USA** / **England**: `\bUS\b` in pronunciation comparisons ("in the US they say schedule", s04e06 MAIN without a US speaker); `\bBritish\b|\bLondon\b` for a place someone lived (x2024-08-02 MAIN).
- **Show-notes hits do not promote accents to MAIN**, but transcript hits do: s03e05 New Zealand "show notes 2 mentions" → MINOR, x2024-06-29 Australia (show notes explicitly: "practice listening to the Australian accent") → MINOR, while s04e04 Australia with 4 hits → MAIN. For accents the show notes ("We have speakers from the US, the UK, Ireland…") are the most reliable source and should give MAIN.

## 6. Topics/language points that are discussed but have no entry

- **Drugs / legalisation** – x2024-05-01 is entirely about legalising marijuana and gets no Topic at all. Crime & Law lacks `legal(is|iz)|\blegal\b|\bdrugs?\b|marijuana|cannabis`.
- **Globalisation** – s03e09 (11:00–15:30, long well-structured answer: travel, internet, English) – 5 hits of "globali…", no entry (Global Issues does not match).
- **Racism / guns** – s04e01: "racial issues in the USA", "people of color", "white supremacy", "availability of firearms" – no entry (could go to Global Issues: `racis|racial|\bguns?\b|firearm`).
- **Buying time / fillers** – explained in s03e05 ("time-buyers"), s03e07 ("stalling expressions"), s04e09 ("that's thrown me"), s04e01 ("it's not really a subject I know a lot about") – a recurring Trevor point with no Language entry. Patterns: `time-buy|buy (yourself |some |a bit of )?time|stalling|give yourself (a few|some) (extra )?seconds|time to think`.
- **Substitution & ellipsis** – s04e05 (substitution as a Cambridge writing criterion), x2024-04-16 (show notes: "substitution words and ellipsis", tested in Use of English Part 2) – no entry.
- **Rhetorical questions** – s04e09 (whole section) – no entry.
- **Intensifiers** – "super" (x2022-10-14), "heck" (s03e09), "pretty damn" (s04e04), "sheer" (s04e06), "at all" (s04e08) – could be patterns of Emphasis & Auxiliaries (`intensif`).
- **Sandwich technique** – s04e02, s04e09 – add `sandwich` to Organising Your Answer.
- **Adverbs** are under-assigned: show notes announce them in s03e04 ("awesome adverbs"), s03e09, s04e01, s04e04 ("top adverbs"), s04e07, s04e10 and Trevor explains utterly, predominantly, drastically, eminently – yet Adverbs is never MAIN and in s03e04/s03e09/s04e04/s04e07 not even present (min 4 too high; a show-notes hit should promote, as it does for Phrasal Verbs/Idioms).
- **Speculating about photos** is a speaking-exam skill with its own section in s03e03, s03e05, s03e07, s03e09; it currently lands under the Topic "Photography & Photos", which is fine, but there is no Exams/Language entry for the language of speculation (`speculat`, `looks like|looks as if|it might be|it could be`).

## 7. Logic

- A show-notes hit makes a Topic MAIN even with 3–4 transcript hits (s04e10 Environment, s03e08 Music, s04e01 Travel); because the show notes include credits and example questions ("regarding things like jobs, Artificial Intelligence or maybe the environment"), show-notes evidence should require at least the entry's `min` in the transcript as well.
- Trevor's fixed intro/outro text (class ads, "buy me a coffee", "happy to help", "if you need help preparing for an exam", "check out Instagram and Facebook") is counted like speaker content; it inflates Help & Kindness, Happiness, Shopping, Technology (Instagram/Facebook → Photography `instagram`), Learning (`\bstudents?\b` in "my students") in every episode. Stripping the recurring ad sentences before counting would remove most MINOR noise.
- Title-matched Topics are always right; title-matched Accents (x2024-04-16, x2024-06-29, x2024-08-02) are right.
