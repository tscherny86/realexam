"""Topics, language points, exams and accents of the Real Exam English wiki.

Each entry creates one article in the vault. Structure:
  name     – title of the article (= file name)
  folder   – sub-folder (Topics, Language, Exams, Accents)
  patterns – regex patterns (case-insensitive) used to search episode titles, show notes and transcripts
  min      – optional: mentions needed in a transcript to count as a main topic (default 3, see
             build_wiki.MIN_MENTIONS); raise it for very common words
  summary  – one-sentence description for the overviews
  body     – explanation (general knowledge, NOT taken from the podcast). What was said in the
             podcast is added by the generator automatically, with episode + minute.

Add new entries here and run `python scripts/build_wiki.py`.
"""

TOPICS = [
    # ------------------------------------------------------------------ Topics (exam subjects)
    {
        "name": "Travel, Holidays & Tourism",
        "folder": "Topics",
        "patterns": [r"\btravel", r"tourism", r"tourist", r"holiday", r"vacation", r"\bcamping\b", r"sightseeing", r"backpack", r"\btrip\b"],
        "summary": "The most common exam topic of all: trips, holidays, mass tourism and the language of getting around.",
        "body": """
**Travel and holidays** turn up in almost every speaking and writing exam, from a B2 First
collaborative task about a school trip to a C2 Proficiency essay on the effects of tourism.

- Useful distinctions: *travel* (uncountable, the activity), *a trip* (one journey), *a journey*
  (the act of going somewhere), *a tour* (organised, several places), *a voyage* (by sea).
- Typical collocations: *set off*, *get away*, *a package holiday*, *off the beaten track*,
  *a tourist trap*, *jet lag*, *travel light*, *soak up the atmosphere*.
- Discussion angles examiners like: **mass tourism vs. local life**, *staycations*, the environmental
  cost of flying, whether travel broadens the mind.
""",
    },
    {
        "name": "Food & Cooking",
        "folder": "Topics",
        "patterns": [r"\bfood\b", r"\bcooking\b", r"\bcook\b", r"cuisine", r"recipe", r"restaurant", r"\bdiet\b", r"vegetarian", r"vegan", r"\bmeal", r"\bdish(es)?\b", r"takeaway"],
        "summary": "Eating habits, cooking, restaurants and diets – a favourite in B2 and C1 speaking tests.",
        "body": """
Food is an easy topic to speak about at length, which is exactly why examiners like it: they can see
how far your vocabulary stretches beyond *delicious* and *tasty*.

- Grading adjectives: *mouth-watering*, *bland*, *greasy*, *rich*, *hearty*, *stodgy*, *spicy*,
  *savoury*, *overcooked*, *underdone*.
- Habits and trends: *eat out*, *grab a bite*, *a balanced diet*, *processed food*, *home-cooked*,
  *comfort food*, *go vegan*, *cut down on sugar*.
- Culture: national dishes, table manners, the rise of food delivery apps and whether cooking skills
  are disappearing.
""",
    },
    {
        "name": "Sport & Exercise",
        "folder": "Topics",
        "patterns": [r"\bsports?\b", r"exercis", r"\bgym\b", r"football", r"fitness", r"workout", r"athlet", r"keep fit", r"\bjogging\b", r"\brunning\b"],
        "summary": "Keeping fit, competitive sport and the role of exercise in a healthy life.",
        "body": """
Exam questions on sport usually go beyond *Which sport do you like?* – you may be asked whether
competitive sport is good for children, whether top athletes earn too much or how to get people to
exercise more.

- Verbs: *do* sport/exercise/yoga, *play* football/tennis (ball and team games), *go* running/swimming
  (-ing activities).
- Vocabulary: *work out*, *warm up*, *take up a sport*, *a couch potato*, *be in good shape*,
  *sedentary lifestyle*, *endurance*, *a personal best*.
- Idioms from sport that are used everywhere: *move the goalposts*, *a level playing field*,
  *the ball is in your court*, *learn the ropes*.
""",
    },
    {
        "name": "Technology & the Internet",
        "folder": "Topics",
        "patterns": [r"technolog", r"\binternet\b", r"\bonline\b", r"smartphone", r"social media", r"\bapps?\b", r"artificial intelligence", r"\bAI\b", r"gadget", r"screen time", r"\bdigital\b"],
        "summary": "Smartphones, social media, AI and how technology changes daily life – a standard C1 topic.",
        "body": """
Technology questions are a safe bet in every exam: *Has technology made our lives easier?*,
*Do people spend too much time online?*, *Will artificial intelligence replace jobs?*

- Vocabulary: *cutting-edge*, *user-friendly*, *obsolete*, *to go viral*, *to scroll through*,
  *to be glued to a screen*, *a digital detox*, *breakthrough*, *to rely on*.
- Pronunciation traps: *technology* (stress on **-no-**), *Wi-Fi*, *YouTube*, *data*.
- Writing: technology essays need a balanced view – convenience and connection versus privacy,
  addiction and the loss of face-to-face contact.
""",
    },
    {
        "name": "Music",
        "folder": "Topics",
        "patterns": [r"\bmusic\b", r"\bsongs?\b", r"concert", r"\bband\b", r"playlist", r"musical instrument", r"\bgig\b", r"\balbum\b"],
        "summary": "Musical taste, concerts and playing an instrument.",
        "body": """
Music is a classic B2 speaking topic and a good source of personal examples for *Part 1* questions.

- Vocabulary: *catchy*, *a tune*, *lyrics*, *live music*, *a gig*, *background music*,
  *to be into (a genre)*, *to have a wide taste in music*, *to play by ear*.
- Discussion: streaming versus buying music, whether music education should be compulsory, why
  tastes change with age.
""",
    },
    {
        "name": "The Environment & Climate Change",
        "folder": "Topics",
        "patterns": [r"environment", r"climate change", r"pollution", r"recycl", r"global warming", r"carbon", r"sustainab", r"\bplastic", r"renewable", r"\bemissions?\b", r"eco-friendly", r"\bgreenhouse"],
        "summary": "Pollution, recycling, climate change and sustainable living – essential for every level.",
        "body": """
Hardly any exam goes by without an environmental question, and C1/C2 essays on climate change are
among the most frequent writing tasks.

- Core vocabulary: *carbon footprint*, *greenhouse gases*, *renewable energy*, *fossil fuels*,
  *deforestation*, *biodegradable*, *to cut down on*, *to run out of*, *to phase out*.
- Collocations: *tackle/combat climate change*, *raise awareness*, *take drastic measures*,
  *irreversible damage*, *a pressing issue*.
- Arguments: individual responsibility vs. government action, economic growth vs. protection,
  whether small changes (recycling, cycling) make a difference.
""",
    },
    {
        "name": "Books & Reading",
        "folder": "Topics",
        "patterns": [r"\bbooks?\b", r"\breading\b", r"\bnovels?\b", r"literature", r"\bauthor", r"library", r"e-?book", r"\bgenre"],
        "summary": "Reading habits, favourite genres and whether books have a future.",
        "body": """
Questions about reading test both vocabulary and the ability to describe something in detail
(*Tell us about a book that influenced you*).

- Vocabulary: *a page-turner*, *gripping*, *a plot twist*, *a bookworm*, *to skim/scan*,
  *to browse*, *non-fiction*, *a best-seller*, *to get through a book*.
- Discussion: printed books vs. e-books, whether young people read less, compulsory reading at school.
""",
    },
    {
        "name": "TV, Film & Entertainment",
        "folder": "Topics",
        "patterns": [r"\bTV\b", r"television", r"\bfilms?\b", r"\bmovies?\b", r"\bseries\b", r"cinema", r"netflix", r"streaming", r"box set", r"\bsitcom", r"documentar"],
        "summary": "Watching habits, streaming, cinema and the quality of television.",
        "body": """
Film and television offer easy personal examples and a lot of lively vocabulary.

- Vocabulary: *binge-watch*, *a cliffhanger*, *a spoiler*, *a box set*, *a remake*, *a sequel*,
  *the cast*, *a plot*, *special effects*, *to be hooked on*.
- Discussion: does television educate or dumb down, reality TV, streaming services replacing cinema,
  subtitles vs. dubbing for language learning.
""",
    },
    {
        "name": "Celebrations & Festivals",
        "folder": "Topics",
        "patterns": [r"celebrat", r"festival", r"christmas", r"birthday", r"wedding", r"\bparty\b", r"\bparties\b", r"new year", r"halloween", r"\beaster\b", r"thanksgiving"],
        "summary": "Birthdays, weddings, Christmas and national festivals – a rich source of cultural vocabulary.",
        "body": """
Celebrations are a common B2 topic (*How do you celebrate New Year?*) and a good way for
examiners to hear cultural comparison.

- Vocabulary: *to throw a party*, *to get together*, *a family gathering*, *fireworks*,
  *a feast*, *to let your hair down*, *to mark an occasion*, *a bank holiday*, *traditional dress*.
- Cultural notes: Christmas crackers and pantomime in the UK, Thanksgiving in the USA, St Patrick's Day
  in Ireland, Guy Fawkes Night, Bonfire Night, *Hogmanay* in Scotland.
""",
    },
    {
        "name": "City & Country Life",
        "folder": "Topics",
        "patterns": [r"countryside", r"city life", r"\burban\b", r"\brural\b", r"village", r"suburb", r"big city", r"small town", r"city centre", r"downtown"],
        "summary": "Living in a big city versus living in the countryside.",
        "body": """
*Would you rather live in a city or in the countryside?* is a question at every level, and it
invites comparatives, conditionals and plenty of descriptive vocabulary.

- City: *hustle and bustle*, *convenient*, *overcrowded*, *cosmopolitan*, *the rat race*,
  *the cost of living*, *commuting*, *nightlife*.
- Country: *peace and quiet*, *fresh air*, *close-knit community*, *in the middle of nowhere*,
  *remote*, *cut off*, *a slower pace of life*.
""",
    },
    {
        "name": "Global Issues",
        "folder": "Topics",
        "patterns": [r"global issue", r"poverty", r"inequality", r"refugee", r"\bwars?\b", r"homeless", r"charity", r"human rights", r"overpopulation", r"famine", r"\bdeveloping countr", r"\bmigration\b"],
        "summary": "Poverty, migration, war and the big problems of the world – typical C1 and C2 essay material.",
        "body": """
Global issues appear mainly in the higher levels, where you are expected to discuss causes,
consequences and solutions in a structured way.

- Vocabulary: *to eradicate poverty*, *the gap between rich and poor*, *aid*, *a humanitarian crisis*,
  *to tackle/address a problem*, *a root cause*, *far-reaching consequences*, *a pressing concern*.
- Essay skills: define the problem, weigh two or three angles, use linking words for cause and
  effect (*as a result*, *consequently*, *owing to*).
""",
    },
    {
        "name": "Shopping & Consumerism",
        "folder": "Topics",
        "patterns": [r"shopping", r"\bshops?\b", r"consumer", r"purchas", r"bargain", r"\bbrands?\b", r"\bretail", r"\bsales?\b", r"second-?hand", r"\bbuy\b", r"\bbought\b"],
        "summary": "Shopping habits, online shopping, brands and consumer society.",
        "body": """
Shopping is a B2 favourite that can be pushed to C1/C2 with questions about consumerism and
advertising.

- Vocabulary: *a bargain*, *a rip-off*, *to splash out*, *to shop around*, *window shopping*,
  *an impulse buy*, *retail therapy*, *a refund*, *a receipt*, *to be worth the money*.
- Discussion: online vs. high-street shopping, fast fashion, whether we buy too much, the influence of
  brands and influencers.
""",
    },
    {
        "name": "Health & Wellbeing",
        "folder": "Topics",
        "patterns": [r"\bhealth", r"illness", r"\bdoctors?\b", r"mental health", r"wellbeing", r"well-being", r"hospital", r"disease", r"\bstress", r"\bdiet\b", r"\bsleep\b", r"junk food"],
        "summary": "Healthy living, illness, mental health and the health service.",
        "body": """
Health questions range from *How do you keep healthy?* (B2) to essays on obesity, mental health or
the cost of public health care (C1/C2).

- Vocabulary: *to come down with*, *to get over an illness*, *a check-up*, *a balanced diet*,
  *to cut down on*, *to be run down*, *burnout*, *a sedentary lifestyle*, *preventive care*.
- Collocations: *lead a healthy life*, *raise awareness of*, *put on/lose weight*, *suffer from*.
""",
    },
    {
        "name": "Friends & Friendship",
        "folder": "Topics",
        "patterns": [r"\bfriends?\b", r"friendship", r"\bmates?\b", r"best friend", r"\bbestie"],
        "summary": "What makes a good friend, keeping in touch and friendships that change over time.",
        "body": """
A gentle B2/C1 topic that is often used to test the vocabulary of personality and relationships.

- Vocabulary: *to get on well with*, *to hit it off*, *to fall out with*, *to keep in touch*,
  *to drift apart*, *a close friend*, *an acquaintance*, *loyal*, *trustworthy*, *through thick and thin*.
- Discussion: online friends vs. real friends, whether it is harder to make friends as an adult,
  quality versus quantity.
""",
    },
    {
        "name": "Free Time & Hobbies",
        "folder": "Topics",
        "patterns": [r"free time", r"leisure", r"\bhobby\b", r"\bhobbies\b", r"pastime", r"spare time", r"\bweekends?\b", r"day off"],
        "summary": "Leisure activities, hobbies and how we spend our weekends.",
        "body": """
Free time is a Part 1 classic (*What do you do in your free time?*), so it pays to have a few
answers ready that go beyond *I like watching TV*.

- Vocabulary: *to take up a hobby*, *to be into something*, *to unwind*, *to chill out*,
  *a lie-in*, *to potter about*, *to get round to doing something*, *to make the most of*.
- Phrases for weekends: *a long weekend*, *a lazy Sunday*, *to catch up on sleep*, *to go out for a meal*.
""",
    },
    {
        "name": "Work & Careers",
        "folder": "Topics",
        "patterns": [r"\bwork\b", r"\bjobs?\b", r"career", r"employ", r"\bboss\b", r"\boffice\b", r"colleague", r"salary", r"profession", r"work-life balance", r"\bretire", r"unemployment", r"\bworkplace\b"],
        "min": 6,
        "summary": "Jobs, careers, the workplace and work-life balance – a C1 Advanced staple.",
        "body": """
Work is one of the most frequent C1 topics: *Is it better to work for a large company or a small
one?*, *How important is job satisfaction?*, *Should people retire later?*

- Vocabulary: *to apply for*, *to be promoted*, *to be made redundant*, *to work overtime*,
  *a nine-to-five job*, *to climb the career ladder*, *job security*, *to work from home*,
  *to burn out*, *a deadline*.
- Confusables: *work* (uncountable) vs. *a job* (countable); *career* is not a *carrera* (race).
""",
    },
    {
        "name": "Communication",
        "folder": "Topics",
        "patterns": [r"communicat", r"text message", r"\btexting\b", r"phone call", r"\bemail", r"\bletters?\b", r"\bwhatsapp\b", r"video call", r"face-to-face", r"\bchat\b"],
        "summary": "How we keep in touch: messaging, calls, social media and face-to-face contact.",
        "body": """
Communication topics ask how technology has changed the way we talk to each other and whether
something has been lost.

- Vocabulary: *to keep in touch*, *to get in touch*, *to lose touch*, *to drop someone a line*,
  *to get back to someone*, *to hang up*, *to put someone through*, *body language*, *small talk*.
- Discussion: emojis and abbreviations, the decline of letter writing, whether people communicate
  more but connect less.
""",
    },
    {
        "name": "Family & Relationships",
        "folder": "Topics",
        "patterns": [r"\bfamily\b", r"families", r"\bparents?\b", r"sibling", r"\bbrothers?\b", r"\bsisters?\b", r"relatives?\b", r"grandparent", r"grandmother", r"grandfather", r"relationship", r"marriage", r"\bmarried\b", r"\bcousins?\b"],
        "min": 5,
        "summary": "Family life, generations, marriage and relationships.",
        "body": """
Family is a staple of every speaking test and a frequent writing topic (*Are family ties weaker
than in the past?*).

- Vocabulary: *extended/nuclear family*, *to bring up / raise children*, *to take after someone*,
  *to look up to*, *to get on with*, *an only child*, *siblings*, *the generation gap*,
  *to settle down*, *to tie the knot*.
- Grammar hook: family stories are perfect for narrative tenses and *used to / would* for past habits.
""",
    },
    {
        "name": "Humour & Comedy",
        "folder": "Topics",
        "patterns": [r"humou?r", r"\bfunny\b", r"\bjokes?\b", r"comedy", r"comedian", r"\blaugh", r"sarcas", r"\bwitty\b", r"\bbanter\b"],
        "summary": "What different cultures find funny, sarcasm, banter and stand-up comedy.",
        "body": """
Humour is a C1/C2 topic that doubles as a cultural lesson: British irony and *banter*, American
stand-up, Irish *slagging* (teasing).

- Vocabulary: *a sense of humour*, *to crack a joke*, *to burst out laughing*, *hilarious*,
  *dry/deadpan humour*, *self-deprecating*, *a pun*, *to take the mickey*, *to not get a joke*.
- Spelling: British *humour / humorous* (no *u* in the adjective), American *humor*.
""",
    },
    {
        "name": "Anger & Emotions",
        "folder": "Topics",
        "patterns": [r"\banger\b", r"\bangry\b", r"annoy", r"frustrat", r"emotion", r"\btemper\b", r"furious", r"\bupset\b", r"\bfeelings?\b", r"lose it", r"\bmood\b"],
        "summary": "Talking about feelings – from mild irritation to losing your temper.",
        "body": """
Emotion vocabulary separates a B2 candidate (*angry*, *sad*, *happy*) from a C1 one
(*livid*, *gutted*, *over the moon*).

- Scale of anger: *irritated* → *annoyed* → *cross* → *furious* → *livid*.
- Expressions: *to lose your temper*, *to fly off the handle*, *to get on someone's nerves*,
  *to drive someone up the wall*, *to bottle things up*, *to let off steam*, *to calm down*.
- Grammar: *-ed* vs. *-ing* adjectives (*I'm annoyed* vs. *it's annoying*).
""",
    },
    {
        "name": "Photography & Photos",
        "folder": "Topics",
        "patterns": [r"\bphotos?\b", r"photograph", r"\bpictures?\b", r"\bcamera", r"selfie", r"instagram", r"\bsnapshot"],
        "summary": "Taking photos, social media pictures and the speaking-exam skill of describing a picture.",
        "body": """
Photos matter twice in exams: as a topic (*Do people take too many photos?*) and as a task –
in B2 First and C1 Advanced Part 2 you **compare two photographs** and speculate about them.

- Speculating language: *it looks as if*, *they might be*, *judging by*, *I'd say*, *perhaps*.
- Vocabulary: *to take/pose for a photo*, *a close-up*, *in the background/foreground*,
  *to capture a moment*, *photogenic*, *to edit/filter*, *a candid shot*.
""",
    },
    {
        "name": "Money & Finance",
        "folder": "Topics",
        "patterns": [r"\bmoney\b", r"financ", r"\bsavings?\b", r"\bspend", r"\bdebt", r"budget", r"\bbank\b", r"\bwealth", r"\bcash\b", r"\bloan", r"\bincome\b", r"\bpocket money\b", r"\bexpensive\b"],
        "min": 5,
        "summary": "Saving, spending, debt and attitudes to money.",
        "body": """
Money questions (*Is it better to save or to spend?*, *Should children get pocket money?*) are
common at every level.

- Vocabulary: *to be broke*, *to be well off*, *to make ends meet*, *to put money aside*,
  *to splash out*, *a loan*, *interest rates*, *a mortgage*, *to live beyond your means*,
  *money doesn't grow on trees*.
- Slang you may hear: *quid*, *grand*, *dosh*, *bucks*.
""",
    },
    {
        "name": "Learning, School & Education",
        "folder": "Topics",
        "patterns": [r"\blearning\b", r"education", r"\bschool", r"\bstudents?\b", r"\bteachers?\b", r"\bstudy", r"universit", r"\bcourse", r"homework", r"\bclassroom", r"\bcurriculum"],
        "min": 6,
        "summary": "School days, learning styles, university and whether education prepares you for life.",
        "body": """
Education is the single most common topic in Cambridge exams, especially in the *for Schools*
versions and in C1 Advanced essays.

- Vocabulary: *to sit/take an exam*, *to pass/fail*, *to revise*, *a subject*, *compulsory*,
  *a gap year*, *tuition fees*, *to drop out*, *lifelong learning*, *to pick something up*.
- Discussion: exams vs. coursework, online learning, school uniforms, which subjects are useful.
""",
    },
    {
        "name": "Fashion & Clothes",
        "folder": "Topics",
        "patterns": [r"fashion", r"\bclothes\b", r"clothing", r"\bdress", r"outfit", r"(?<!-)\bstyle\b", r"\bwear", r"\bbrands?\b", r"designer", r"\btrendy\b"],
        "min": 5,
        "summary": "Clothes, personal style and the fashion industry.",
        "body": """
Fashion lets examiners test descriptive vocabulary and opinions on consumer culture.

- Vocabulary: *to dress up/down*, *smart/casual*, *to be in/out of fashion*, *fast fashion*,
  *a wardrobe*, *to go with*, *to suit someone*, *to fit*, *second-hand / vintage*, *a fashion victim*.
- Discussion: school uniforms, whether appearance matters, the environmental cost of fast fashion.
""",
    },
    {
        "name": "Animals & Pets",
        "folder": "Topics",
        "patterns": [r"\banimals?\b", r"\bpets?\b", r"\bdogs?\b", r"\bcats?\b", r"wildlife", r"\bzoos?\b", r"species", r"endangered", r"\bvegetarian"],
        "min": 4,
        "summary": "Pets, wildlife, zoos and animal rights.",
        "body": """
From *Do you have a pet?* to C2 debates on animal testing and zoos – animals cover all levels.

- Vocabulary: *to keep a pet*, *a stray*, *to put down*, *endangered species*, *to go extinct*,
  *in captivity*, *in the wild*, *animal welfare*, *cruelty*, *a vet*.
- Idioms: *the elephant in the room*, *let the cat out of the bag*, *raining cats and dogs*,
  *a dark horse*, *to smell a rat*.
""",
    },
    {
        "name": "Fame & Celebrity",
        "folder": "Topics",
        "patterns": [r"\bfame\b", r"\bfamous\b", r"celebrit", r"\bstars?\b", r"paparazzi", r"\bprivacy\b", r"influencer", r"\bidol"],
        "summary": "Celebrities, privacy and whether fame is worth having.",
        "body": """
A C1 classic: *Do celebrities deserve their privacy?*, *Would you like to be famous?*

- Vocabulary: *to be in the public eye*, *to shoot to fame*, *a household name*,
  *fifteen minutes of fame*, *to hit the headlines*, *intrusive*, *a role model*, *the price of fame*.
""",
    },
    {
        "name": "Culture & Traditions",
        "folder": "Topics",
        "patterns": [r"\bculture", r"cultural", r"tradition", r"\bcustoms?\b", r"heritage", r"\bstereotype", r"culture shock"],
        "min": 5,
        "summary": "Cultural differences, traditions and stereotypes between English-speaking countries.",
        "body": """
Cultural comparison is built into the podcast: speakers from Ireland, the UK, the USA, Australia,
New Zealand and South Africa answer the same questions very differently.

- Vocabulary: *culture shock*, *to be steeped in tradition*, *to preserve/uphold a tradition*,
  *to die out*, *a stereotype*, *to broaden your horizons*, *a melting pot*, *etiquette*.
""",
    },
    {
        "name": "Change & Life Changes",
        "folder": "Topics",
        "patterns": [r"\bchang(e|es|ed|ing)\b", r"turning point", r"\bmove(d)? abroad", r"\bnew chapter"],
        "min": 12,
        "summary": "Big life changes, moving abroad and how people deal with change.",
        "body": """
*Tell us about a change that affected you* is a typical C1 long-turn question; it rewards narrative
tenses and reflective language.

- Vocabulary: *a turning point*, *to turn over a new leaf*, *to adapt to*, *to be set in your ways*,
  *to resist change*, *to embrace change*, *out of your comfort zone*, *in hindsight*.
""",
    },
    {
        "name": "Happiness",
        "folder": "Topics",
        "patterns": [r"happiness", r"\bhappy\b", r"\bjoy\b", r"contentment", r"\bcontent\b", r"satisf", r"fulfil"],
        "min": 5,
        "summary": "What makes people happy and whether money can buy it.",
        "body": """
Happiness is a reflective C1/C2 topic that invites abstract nouns and hedging language.

- Vocabulary: *over the moon*, *on cloud nine*, *to make the most of*, *fulfilling*,
  *contentment*, *peace of mind*, *to count your blessings*, *materialistic*, *a sense of purpose*.
""",
    },
    {
        "name": "Crime & Law",
        "folder": "Topics",
        "patterns": [r"\bcrimes?\b", r"criminal", r"police", r"\btheft\b", r"\bsteal", r"\bstolen\b", r"burglar", r"\blaws?\b", r"prison", r"murder", r"illegal", r"\bpunish", r"shoplift", r"\bjail\b", r"\bfine[sd]?\b"],
        "summary": "Types of crime, punishment and how safe different countries feel.",
        "body": """
Crime is a frequent C1 Advanced topic with a lot of specific vocabulary to learn.

- Crimes: *burglary*, *shoplifting*, *pickpocketing*, *fraud*, *vandalism*, *mugging*, *drink-driving*.
- People: *a burglar*, *a thief*, *a witness*, *a judge*, *the jury*, *the defendant*.
- Process: *to commit a crime*, *to be arrested/charged/convicted*, *to be sentenced to*,
  *a fine*, *community service*, *to get away with*.
- Discussion: harsher sentences vs. rehabilitation, CCTV and privacy, why crime rates rise or fall.
""",
    },
    {
        "name": "Languages & Language Learning",
        "folder": "Topics",
        "patterns": [r"\blanguages?\b", r"bilingual", r"native speaker", r"learn(ing)? English", r"mother tongue", r"\bfluent"],
        "min": 8,
        "summary": "Learning languages, being bilingual and the experience of living in another language.",
        "body": """
A topic every candidate can speak about from experience – which is why examiners expect a strong
answer here.

- Vocabulary: *to pick up a language*, *to be fluent in*, *to get by in*, *a native speaker*,
  *mother tongue*, *to brush up on*, *to immerse yourself*, *rusty*, *to lose your accent*.
- Discussion: the best age to learn a language, whether English will stay the global language,
  learning in the classroom vs. abroad.
""",
    },
    {
        "name": "Home & Housing",
        "folder": "Topics",
        "patterns": [r"\bhomes?\b", r"\bhouses?\b", r"\bflats?\b", r"apartment", r"\brent", r"mortgage", r"housing", r"neighbou?r", r"\bmove(d)? house", r"\bhousework\b", r"\bchores?\b"],
        "min": 6,
        "summary": "Where and how we live: houses, flats, renting, neighbours and housework.",
        "body": """
Home is a B2 Part 1 favourite (*Describe your home*) and a C1 discussion topic (*Should young people
leave home early?*).

- Vocabulary: *a semi-detached/terraced house*, *a cosy flat*, *spacious*, *cramped*,
  *to move in/out*, *to do up a house*, *a mortgage*, *to rent*, *a landlord*, *household chores*.
- Spelling and sound: *house* /haʊs/ vs. *houses* /ˈhaʊzɪz/.
""",
    },
    {
        "name": "Weather & Seasons",
        "folder": "Topics",
        "patterns": [r"weather", r"\brain", r"\bsnow", r"\bstorms?\b", r"\bsunny\b", r"temperature", r"forecast", r"\bsummer\b", r"\bwinter\b", r"heatwave", r"\bwindy\b", r"\bcloudy\b"],
        "min": 5,
        "summary": "Talking about the weather – the great British conversation starter.",
        "body": """
Weather is small-talk material in English-speaking countries and a reliable Part 1 question.

- Vocabulary: *drizzle*, *a downpour*, *pouring*, *chilly*, *freezing*, *scorching*, *muggy*,
  *overcast*, *a heatwave*, *to clear up*, *to brighten up*.
- Idioms: *under the weather*, *to save for a rainy day*, *to steal someone's thunder*,
  *every cloud has a silver lining*.
""",
    },
    {
        "name": "Art & Creativity",
        "folder": "Topics",
        "patterns": [r"\bart\b", r"\bartists?\b", r"painting", r"museum", r"gallery", r"creativ", r"sculpture", r"\bdesign\b", r"\bdrawing\b", r"\bartistic\b"],
        "min": 4,
        "summary": "Art, museums and whether creativity can be taught.",
        "body": """
Art appears in C1 and C2 speaking tests and in reading texts; creativity is a popular essay angle
(*Is creativity more important than knowledge?*).

- Vocabulary: *a masterpiece*, *an exhibition*, *abstract*, *to appreciate*, *to be gifted*,
  *to think outside the box*, *to come up with*, *inspiration*, *to express yourself*.
""",
    },
    {
        "name": "Transport & Traffic",
        "folder": "Topics",
        "patterns": [r"transport", r"traffic", r"\bbus(es)?\b", r"\btrains?\b", r"\bcars?\b", r"\bdriving\b", r"commut", r"\bbikes?\b", r"cycling", r"\bflights?\b", r"\bplanes?\b", r"congestion", r"\bparking\b"],
        "min": 5,
        "summary": "Public transport, cars, cycling and how to get around cities.",
        "body": """
Transport questions are common at B2 and C1 (*Should cars be banned from city centres?*).

- Vocabulary: *to get on/off*, *to get in/out of a car*, *rush hour*, *a traffic jam*,
  *to commute*, *a cycle lane*, *to miss/catch a train*, *public transport* (uncountable, no *s*).
- Confusables: *travel* (verb/uncountable noun), *a journey*, *a trip*; *drive* vs. *ride*.
""",
    },
    {
        "name": "Parenting & Children",
        "folder": "Topics",
        "patterns": [r"parenting", r"\bparents?\b", r"\bchild\b", r"\bchildren\b", r"\bkids?\b", r"upbringing", r"toddler", r"\bbab(y|ies)\b", r"childhood", r"teenager"],
        "min": 6,
        "summary": "Bringing up children, childhood then and now, and what children need.",
        "body": """
Parenting is a C1/C2 topic; childhood memories are a B2 long-turn favourite.

- Vocabulary: *to bring up / raise*, *strict*, *lenient*, *to spoil*, *to discipline*,
  *a role model*, *to set boundaries*, *helicopter parents*, *to grow up*, *to look back on*.
- Grammar hook: *used to* and *would* for childhood habits, *wish* and *if only* for regrets.
""",
    },
    {
        "name": "History & the Past",
        "folder": "Topics",
        "patterns": [r"\bhistory\b", r"historical", r"ancestor", r"\bcentur(y|ies)\b", r"in the past", r"\bdecades?\b", r"the good old days", r"\bnostalgi"],
        "min": 5,
        "summary": "Learning from history and comparing the past with the present.",
        "body": """
History questions (*Is it important to learn history?*, *Was life better in the past?*) test
past tenses and the language of comparison.

- Vocabulary: *to look back*, *in hindsight*, *the good old days*, *to date back to*,
  *a turning point*, *to learn from mistakes*, *bygone*, *to romanticise the past*.
""",
    },
    {
        "name": "The Future & Predictions",
        "folder": "Topics",
        "patterns": [r"\bthe future\b", r"\bpredict", r"in (ten|twenty|fifty|\d+) years", r"\bfuturistic\b", r"\brobots?\b", r"\bnext generation\b", r"\bforesee"],
        "min": 6,
        "summary": "Predictions, plans and what the world might look like in a few decades.",
        "body": """
Future questions test modal verbs and future forms: *will*, *going to*, *might*, *is likely to*,
*is bound to*, future continuous and future perfect.

- Vocabulary: *in the long run*, *foreseeable future*, *to look forward to*, *to be on the verge of*,
  *a breakthrough*, *to pave the way for*, *to become obsolete*.
""",
    },
    {
        "name": "Space & Science",
        "folder": "Topics",
        "patterns": [r"\bspace\b", r"planet", r"astronaut", r"\bnasa\b", r"\bmoon\b", r"\bmars\b", r"universe", r"galax", r"rocket", r"\bscience\b", r"scientist", r"\bstars?\b", r"space exploration"],
        "min": 4,
        "summary": "Space exploration, science and whether the money is well spent.",
        "body": """
Space is less common than other topics but an excellent C1/C2 discussion (*Is space exploration
a waste of money?*).

- Vocabulary: *to launch*, *to orbit*, *a mission*, *gravity*, *a telescope*, *to colonise*,
  *out of this world*, *to reach for the stars*, *a breakthrough*.
""",
    },
    {
        "name": "Manners & Politeness",
        "folder": "Topics",
        "patterns": [r"\bmanners\b", r"polite", r"\brude", r"etiquette", r"\brespect", r"\bcourtesy\b", r"\bqueue", r"\bimpolite\b", r"\bsay please\b"],
        "min": 4,
        "summary": "Good and bad manners across English-speaking cultures.",
        "body": """
Manners are a rich cultural topic: queuing in Britain, *please and thank you*, tipping in the USA,
small talk and how direct you can be.

- Vocabulary: *to mind your manners*, *well-mannered*, *rude*, *courteous*, *to hold the door*,
  *to jump the queue*, *to take your shoes off*, *a faux pas*.
""",
    },
    {
        "name": "Relaxing & Stress",
        "folder": "Topics",
        "patterns": [r"\brelax", r"\bchill", r"unwind", r"\bstress", r"\bcalm\b", r"meditat", r"\byoga\b", r"\bswitch off\b", r"\btake it easy\b"],
        "min": 4,
        "summary": "How people relax, switch off and cope with stress.",
        "body": """
A gentle B2/C1 topic with plenty of phrasal verbs.

- Vocabulary: *to unwind*, *to chill out*, *to switch off*, *to put your feet up*, *to take it easy*,
  *laid-back*, *stressed out*, *to be under pressure*, *to let off steam*, *me-time*.
""",
    },
    {
        "name": "Advertising & Marketing",
        "folder": "Topics",
        "patterns": [r"advert", r"\bads?\b", r"commercial", r"marketing", r"\bbrands?\b", r"influencer", r"billboard", r"\bslogan", r"\bsponsor", r"\bpromot"],
        "min": 4,
        "summary": "How advertising works on us and whether it should be restricted.",
        "body": """
Advertising is a C1 Advanced favourite, often linked to children, social media and consumerism.

- Vocabulary: *to target*, *a campaign*, *catchy*, *misleading*, *to endorse*, *product placement*,
  *to be bombarded with*, *brand loyalty*, *to manipulate*, *subliminal*.
- Discussion: should advertising to children be banned, influencers vs. traditional ads.
""",
    },
    {
        "name": "Hometown & Places",
        "folder": "Topics",
        "patterns": [r"hometown", r"home town", r"\bgrew up\b", r"where (I'm|I am|you're|you are) from", r"\bborn in\b", r"\bmy town\b", r"\bneighbourhood\b", r"\bneighborhood\b"],
        "min": 4,
        "summary": "Describing where you come from – one of the first questions in any speaking exam.",
        "body": """
*Where are you from?* opens almost every speaking test, so a confident, detailed answer makes a
good first impression.

- Vocabulary: *a bustling town*, *a sleepy village*, *picturesque*, *industrial*, *run-down*,
  *up-and-coming*, *on the outskirts*, *within walking distance*, *a close-knit community*.
""",
    },
    {
        "name": "News & Media",
        "folder": "Topics",
        "patterns": [r"\bnews\b", r"journalis", r"newspaper", r"headline", r"\bmedia\b", r"fake news", r"\bthe press\b", r"\bbroadcast", r"\bcurrent affairs\b"],
        "min": 4,
        "summary": "How we get the news, fake news and the role of journalists.",
        "body": """
News and media are frequent C1/C2 topics, including the reliability of social media as a news source.

- Vocabulary: *to keep up with the news*, *breaking news*, *a headline*, *to make the news*,
  *biased*, *fake news*, *a reliable source*, *to go viral*, *the tabloids*, *freedom of the press*.
- Grammar: *news* is uncountable (*the news is…*, *a piece of news*).
""",
    },
    {
        "name": "Extremes & Adventure",
        "folder": "Topics",
        "patterns": [r"\bextreme", r"adventur", r"adrenaline", r"\brisks?\b", r"\bdaring\b", r"marathon", r"\bthrill", r"\bdanger"],
        "min": 4,
        "summary": "Extreme experiences, risk-taking and adrenaline sports.",
        "body": """
Stories about extreme experiences are perfect material for narrative tenses, inverted conditionals
and dramatic vocabulary.

- Vocabulary: *to push yourself to the limit*, *an adrenaline rush*, *to take risks*,
  *hair-raising*, *gruelling*, *to be out of your depth*, *to go to extremes*.
""",
    },
    {
        "name": "Complaining & Customer Service",
        "folder": "Topics",
        "patterns": [r"complain", r"complaint", r"customer service", r"\brefund", r"\bwhing", r"\bmoan", r"\bgrumbl"],
        "min": 3,
        "summary": "Making complaints, customer service and a nation of grumblers.",
        "body": """
Complaining is both a speaking topic and a writing task: a **letter of complaint** is a classic
B2 First and C1 Advanced writing question.

- Vocabulary: *to make/lodge a complaint*, *to be entitled to a refund*, *unacceptable*,
  *I was appalled*, *to put up with*, *to kick up a fuss*, *to moan*, *to whinge* (informal).
- Formal letter phrases: *I am writing to express my dissatisfaction with…*, *I would appreciate it
  if…*, *I look forward to your prompt reply.*
""",
    },
    {
        "name": "Motivation & Goals",
        "folder": "Topics",
        "patterns": [r"motivat", r"\bgoals?\b", r"ambition", r"disciplin", r"procrastinat", r"\binspir", r"\bachiev", r"\bdetermin"],
        "min": 4,
        "summary": "Staying motivated, setting goals and overcoming procrastination.",
        "body": """
Motivation is a reflective C1 topic with useful vocabulary for essays about work, study and sport.

- Vocabulary: *to set a goal*, *to stay focused*, *to keep going*, *to put off*, *self-discipline*,
  *a sense of achievement*, *driven*, *to give up*, *to stick to*, *willpower*.
""",
    },
    {
        "name": "Luck & Chance",
        "folder": "Topics",
        "patterns": [r"\bluck\b", r"\blucky\b", r"\bunlucky\b", r"fortune", r"superstit", r"lottery", r"\bchance\b", r"\bcoincidence\b"],
        "min": 4,
        "summary": "Luck, superstitions, the lottery and whether success is down to chance.",
        "body": """
A fun C1 topic that produces a lot of idioms.

- Vocabulary: *a stroke of luck*, *by sheer luck*, *to be down to luck*, *touch wood*,
  *fingers crossed*, *a lucky charm*, *to push your luck*, *beginner's luck*, *to win the lottery*.
""",
    },
    {
        "name": "Help & Kindness",
        "folder": "Topics",
        "patterns": [r"\bhelp(ing|ed|s)?\b", r"kindness", r"volunteer", r"\bfavou?rs?\b", r"charity", r"generous", r"\bgive back\b", r"\bgood deed"],
        "min": 8,
        "summary": "Helping others, volunteering and acts of kindness.",
        "body": """
Help is a topic bursting with phrasal verbs: *help out*, *give a hand*, *pitch in*, *chip in*,
*step in*, *look after*, *see someone through*.

- Vocabulary: *to lend a hand*, *to do someone a favour*, *to go out of your way*,
  *to volunteer*, *a good Samaritan*, *to return the favour*, *altruistic*.
""",
    },
    {
        "name": "Priorities & Decisions",
        "folder": "Topics",
        "patterns": [r"priorit", r"decision", r"\bdecide", r"\bchoices?\b", r"\bchoose\b", r"\bdilemma\b", r"\bweigh up\b", r"\bmake up (my|your|his|her) mind\b"],
        "min": 4,
        "summary": "Making decisions, setting priorities and weighing things up.",
        "body": """
Decision-making is a C1/C2 topic that pairs naturally with conditionals, the passive and the past
perfect (*If I had known…*).

- Vocabulary: *to make up your mind*, *to weigh up the pros and cons*, *to go with your gut*,
  *a snap decision*, *to put something first*, *to be torn between*, *to think twice*,
  *to sleep on it*, *in two minds*.
""",
    },
    # ------------------------------------------------------------------ Language (grammar & vocabulary)
    *[
        {"name": n, "folder": "Language", "patterns": p, "summary": s, "body": b, **({"min": m} if m else {})}
        for n, p, s, b, m in [
            ("Phrasal Verbs", [r"phrasal verb"], "Verb + particle combinations (get on, put off, come up with) – the heart of natural spoken English.", """
**Phrasal verbs** are verbs combined with a particle (*up, out, on, off, through…*) whose meaning is
often not obvious from the parts: *put up with* = tolerate, *come up with* = think of.

- They dominate informal speech and are a key marker of B2+ fluency. Formal writing often prefers a
  single-word equivalent (*tolerate*, *devise*).
- Grammar: separable (*turn the light off / turn off the light*) vs. inseparable (*look after the
  kids*); with a pronoun the object goes between (*turn it off*).
- Exam tip: learn them in topic groups (work, relationships, money) and in context, not as lists.
""", None),
            ("Idioms & Expressions", [r"\bidioms?\b", r"idiomatic", r"\bexpressions?\b", r"\bsaying\b"], "Fixed expressions whose meaning is figurative – used in every episode of the podcast.", """
**Idioms** are fixed phrases with a figurative meaning: *to be over the moon*, *to hit the nail on the
head*, *once in a blue moon*.

- Cambridge examiners reward natural, correctly used idioms; forced or wrong ones cost marks.
  Use the ones you have heard in context and are sure about.
- Many idioms are informal; in a formal essay keep to neutral expressions.
""", 5),
            ("Collocations", [r"collocat", r"go(es)? together with", r"\bgo with\b"], "Words that naturally go together (make a decision, heavy rain, strong coffee).", """
**Collocations** are word partnerships native speakers use automatically: *make a mistake* (not *do*),
*heavy traffic*, *a strong accent*, *bitterly cold*.

- They are tested directly in *Use of English* (Part 1 multiple choice) and indirectly in
  speaking and writing marks.
- Learn verb + noun (*take a photo*), adjective + noun (*a narrow escape*) and adverb + adjective
  (*deeply disappointed*) pairs.
""", None),
            ("Conditionals", [r"conditional", r"\bif I (had|were)\b", r"\bhad I\b", r"\bwere I\b", r"\bunless\b", r"\bprovided that\b"], "Zero, first, second, third and mixed conditionals, plus inverted forms for C1/C2.", """
- **Zero**: facts (*If you heat ice, it melts*). **First**: real future (*If it rains, we'll stay in*).
- **Second**: unreal present/future (*If I won the lottery, I'd travel*). **Third**: unreal past
  (*If I had known, I would have come*).
- **Mixed**: past condition, present result (*If I had studied medicine, I'd be a doctor now*).
- **Inverted** (C1/C2, formal): *Had I known…*, *Were I you…*, *Should you need anything…*.
- Alternatives to *if*: *unless*, *provided that*, *as long as*, *in case*, *otherwise*.
""", None),
            ("Cleft Sentences", [r"\bcleft"], "What I love about English is… – sentences that put emphasis on one part.", """
**Cleft sentences** split a simple sentence to highlight one element:

- *It*-cleft: *It was Trevor who asked the question.*
- *What*-cleft: *What I really need is a holiday.* / *What surprised me was the price.*
- Other forms: *The reason (why) I left was…*, *All I want is…*, *The thing is…*
- They are very common in natural speech and earn marks for range in C1/C2 speaking and writing.
""", None),
            ("Inversion", [r"\binversion\b", r"\binverted\b", r"\bnever have I\b", r"\bnot only\b", r"\bno sooner\b", r"\brarely\b", r"\bseldom\b", r"\bunder no circumstances\b", r"\blittle did\b"], "Never have I seen… – putting the auxiliary before the subject for emphasis.", """
**Inversion** after negative or limiting adverbials is a hallmark of formal, advanced English:

- *Never have I seen such a mess.* *Not only did he arrive late, but he also forgot the tickets.*
- *No sooner had we sat down than the phone rang.* *Rarely do you find such generosity.*
- *Little did she know…*, *Under no circumstances should you…*, *Only then did I realise…*
- Great for C1/C2 essays and reviews, used sparingly (one or two per text).
""", None),
            ("Passive Voice", [r"\bpassive\b", r"\bget\s+\w+ed\b", r"\bhave (something|it) done\b", r"causative"], "The passive and causative structures (have something done).", """
The **passive** moves the focus from the doer to the action or result: *The decision was made last
week.* It is common in formal writing, reports and news.

- Advanced forms: *It is said that…*, *He is thought to have left*, passive with modals (*should be
  done*), passive infinitives and gerunds (*to be told*, *being watched*).
- **Causative**: *have/get something done* (*I had my car repaired*) – frequently tested in
  Use of English key-word transformations.
- Informal *get*-passive: *He got sacked.*
""", None),
            ("Past Perfect & Narrative Tenses", [r"past perfect", r"narrative tense", r"\bpluperfect\b", r"past continuous", r"past simple", r"\bused to\b", r"\bwould\b.*\bevery\b"], "Telling stories: past simple, past continuous, past perfect and used to / would.", """
Exam stories (*Tell us about a time when…*) are judged on how well you handle the **narrative tenses**:

- **Past simple** for the main events, **past continuous** for background actions in progress,
  **past perfect** for what happened earlier (*By the time we arrived, the show had started*).
- **Used to / would** for past habits (*We would go to the beach every summer*); *would* not for
  past states (*I used to be shy*, not *would be shy*).
- Sequencing language: *at first*, *meanwhile*, *eventually*, *in the end*, *looking back*.
""", None),
            ("Question Tags", [r"question tags?", r"tag questions?"], "…, isn't it? – checking information or inviting agreement.", """
**Question tags** turn a statement into a question: *It's cold, isn't it?* *You haven't seen him,
have you?*

- Positive statement → negative tag, negative statement → positive tag; the tag uses the auxiliary.
- Tricky ones: *I'm late, aren't I?*, *Let's go, shall we?*, *Don't forget, will you?*
- Intonation: falling tag = you expect agreement; rising tag = a real question.
""", None),
            ("Comparatives & Superlatives", [r"comparative", r"superlative", r"\bfar more\b", r"\bby far\b", r"\bnowhere near\b", r"\bthe more .* the more\b"], "Comparing things precisely: far better, nowhere near as good, the more… the more.", """
Beyond *bigger* and *the biggest*, exams look for **modified comparisons**:

- *far/much/considerably/slightly* + comparative; *by far the best*; *nowhere near as expensive as*;
  *not nearly as*; *just as… as*; *twice as big as*.
- *The more you practise, the easier it gets.* *It's getting harder and harder.*
- Spelling: *bigger*, *happier*, *more modern*; irregular: *further*, *elder/eldest*, *less/least*.
""", None),
            ("Adverbs", [r"\badverbs?\b", r"\badverbial\b", r"\b\w+ly\b.*\badverb"], "Adverbs of degree, manner and attitude that make speech sound natural and precise.", """
**Adverbs** show how well you can shade meaning: *utterly exhausted*, *absolutely stunning*,
*slightly annoyed*, *frankly*, *admittedly*, *surprisingly*.

- Gradable vs. ungradable adjectives: *very tired* but *absolutely exhausted* (not *very exhausted*).
- Sentence adverbs for opinion: *Honestly*, *Personally*, *Arguably*, *Undoubtedly*.
- Position matters: *only*, *even*, *just* change meaning depending on where they go.
""", 4),
            ("Adjectives & Compound Adjectives", [r"compound adjective", r"\badjectives?\b", r"\bhyphenat", r"\bwell-known\b", r"\btime-consuming\b", r"\bmouth-watering\b"], "Strong adjectives and compound adjectives (time-consuming, well-off, mouth-watering).", """
- **Strong (extreme) adjectives** replace *very* + adjective: *very good* → *superb*, *very tired* →
  *exhausted*, *very big* → *enormous*.
- **Compound adjectives** combine two words with a hyphen: *time-consuming*, *well-known*,
  *a ten-year-old boy* (no plural *years* before a noun), *mouth-watering*, *long-lasting*.
- Order of adjectives: opinion → size → age → shape → colour → origin → material (*a lovely little old
  wooden box*).
""", 4),
            ("Connectors & Linking Words", [r"connector", r"linking words?", r"\blinkers?\b", r"discourse marker", r"cohesi", r"\bfurthermore\b", r"\bnevertheless\b", r"\bwhereas\b", r"\bhowever\b"], "Linking ideas so that essays and answers flow: however, whereas, furthermore, consequently.", """
**Cohesion** is one of the four writing criteria in Cambridge exams, so linking words are worth marks.

- Contrast: *however*, *whereas*, *although*, *despite / in spite of* + noun or -ing, *nevertheless*.
- Addition: *furthermore*, *moreover*, *in addition*, *what's more*, *not only… but also*.
- Cause and result: *consequently*, *as a result*, *owing to*, *hence*, *therefore*.
- Spoken discourse markers: *well*, *actually*, *to be honest*, *the thing is*, *anyway*.
""", 4),
            ("Relative Clauses", [r"relative clause", r"relative pronoun", r"\bdefining\b", r"non-defining", r"\bwhereby\b", r"\bwhom\b"], "Who, which, that, whose, whereby – defining and non-defining clauses.", """
- **Defining** clauses identify which one (*The man who called was my boss* – no commas).
- **Non-defining** clauses add extra information (*My boss, who lives in Cork, called* – commas,
  no *that*).
- Advanced: *whose*, *whom*, *whereby*, *in which case*, reduced relatives (*the people living next
  door*), *which* referring to a whole clause (*He was late, which annoyed everyone*).
""", None),
            ("Modal Verbs", [r"\bmodal", r"\bmust have\b", r"\bcan't have\b", r"\bmight have\b", r"\bshould have\b", r"\bought to\b", r"\bneedn't\b"], "Must, might, can't, should have – obligation, possibility and deduction.", """
- Obligation and advice: *must*, *have to*, *should*, *ought to*, *needn't*, *had better*.
- Deduction: *must be* (sure), *might/may/could be* (possible), *can't be* (impossible).
- **Modals in the past**: *must have left*, *can't have seen*, *should have told me* (regret),
  *needn't have worried* – a favourite in key-word transformations.
""", None),
            ("Reported Speech", [r"reported speech", r"indirect speech", r"reporting verbs?", r"\bhe said that\b", r"\bshe told me\b"], "Reporting what people said, with tense backshift and reporting verbs.", """
- Backshift: *"I'm tired" → She said she was tired.* Modals and time words change too
  (*will → would*, *tomorrow → the next day*).
- **Reporting verbs** with their patterns are tested heavily: *suggest doing*, *refuse to do*,
  *accuse someone of doing*, *apologise for*, *deny doing*, *insist on*, *warn someone not to*.
""", None),
            ("Pronunciation", [r"pronunciation", r"pronounc", r"\bword stress\b", r"\bstress(ed)? (on|the)\b", r"intonation", r"syllable", r"\bsilent letter", r"\bschwa\b", r"\bsounds? like\b"], "Word stress, silent letters, intonation and the sounds learners get wrong.", """
Pronunciation is one of the four speaking criteria. Examiners look for **individual sounds**,
**word stress**, **sentence stress** and **intonation**, not for a native accent.

- Classic traps: *comfortable* /ˈkʌmftəbl/, *vegetable* /ˈvedʒtəbl/, *clothes* /kləʊðz/,
  *recipe* /ˈresəpi/, *Wednesday*, silent letters in *climb, island, knife, debt*.
- Word stress changes meaning: *REcord* (noun) vs. *reCORD* (verb), *PREsent / preSENT*.
- The **schwa** /ə/ in unstressed syllables is the most common sound in English.
""", None),
            ("Word Formation", [r"word formation", r"\bsuffix", r"\bprefix", r"portmanteau", r"\bnoun form\b", r"\badjective form\b", r"word family"], "Prefixes, suffixes and word families – tested directly in Use of English Part 3.", """
**Word formation** (Use of English Part 3) asks you to change a given word to fit a gap:
*succeed → success → successful → unsuccessfully*.

- Suffixes: *-ment, -ness, -ity, -tion* (nouns); *-ful, -less, -ive, -able* (adjectives);
  *-ly* (adverbs); *-ise/-ize, -en* (verbs).
- Prefixes: *un-, in-, im-, il-, ir-, dis-, mis-, over-, under-, re-*.
- **Portmanteau** words blend two words: *brunch*, *glamping*, *staycation*, *smog*.
""", None),
            ("Prepositions", [r"\bprepositions?\b", r"dependent preposition", r"\binterested in\b", r"\bdepend on\b", r"\bon time\b", r"\bin time\b", r"\bat the end\b", r"\bin the end\b"], "Dependent prepositions and the small words that cause big mistakes.", """
Prepositions are a constant source of errors, and **dependent prepositions** (*depend on*,
*interested in*, *good at*, *responsible for*) appear in every Use of English paper.

- Time: *on Monday*, *in May*, *at night*, *on time* (punctual) vs. *in time* (early enough).
- Place: *at home*, *in the city*, *on the bus*, *at the end* (position) vs. *in the end* (finally).
- Verb + preposition: *arrive in/at* (never *to*), *listen to*, *agree with someone / on something*.
""", 4),
            ("Emphasis & Auxiliaries", [r"\bemphasis\b", r"\bemphatic\b", r"auxiliary verb", r"\bemphasi[sz]e\b", r"\bI do (think|like|love|believe)\b", r"\bdo have\b", r"\breally\b.*\bemphasis\b"], "I DO think…, really, so/such – adding emphasis to what you say.", """
Ways to **add emphasis**:

- Emphatic auxiliary: *I do like it*, *She did warn you*, *It does matter.*
- *So / such*: *so quickly*, *such a mess*; *what a…!*, *how…!*
- Cleft sentences and inversion (see their own articles), *the very*, *at all*, *whatsoever*.
- Stress in speech: *really* changes meaning with position (*I really don't like it* vs.
  *I don't really like it*).
""", None),
            ("Confusing Words & Homophones", [r"homophone", r"homonym", r"confusing words?", r"\beither\b.*\bneither\b", r"\bcommonly confused\b", r"\bfalse friend", r"\baffect\b.*\beffect\b", r"\bthere, their\b", r"\blose\b.*\bloose\b"], "Either/neither, affect/effect, false friends and words that sound the same.", """
- **Homophones**: *their / there / they're*, *weather / whether*, *bear / bare*, *piece / peace*.
- Classic confusions: *affect* (verb) / *effect* (noun), *lose* / *loose*, *lend* / *borrow*,
  *fun* / *funny*, *sensible* / *sensitive*, *actually* (in fact, not *currently*).
- *Either… or*, *neither… nor*; *so do I* / *neither do I* / *me neither*.
- **False friends** for Spanish speakers: *embarrassed* ≠ *embarazada*, *assist* ≠ *asistir*,
  *career* ≠ *carrera*, *library* ≠ *librería*.
""", None),
            ("Common Mistakes", [r"common (mistakes?|errors?)", r"\bmistakes?\b", r"\berrors?\b", r"\bpeople (often|always) say\b", r"\bdon't say\b", r"\bincorrect"], "The errors examiners hear again and again – and how to avoid them.", """
Typical mistakes at B2–C2:

- *People is* → *people are*; *informations* → *information* (uncountable); *advices* → *advice*.
- *I am agree* → *I agree*; *depend of* → *depend on*; *explain me* → *explain to me*.
- *Since three years* → *for three years*; *I have 20 years* → *I am 20*.
- *Make* vs. *do*: *make a decision, do homework*; *say* vs. *tell*: *tell me, say something*.
- Overusing *very* and *a lot of* instead of stronger vocabulary.
""", 4),
            ("Binomial Pairs", [r"binomial", r"\bsafe and sound\b", r"\bsick and tired\b", r"\bwear and tear\b", r"\bodds and ends\b", r"\bups and downs\b", r"\bpros and cons\b"], "Fixed pairs like 'safe and sound', 'sick and tired', 'ups and downs'.", """
**Binomial pairs** are fixed expressions of two words joined by *and* or *or*, always in the same order:

- *safe and sound*, *sick and tired*, *pros and cons*, *ups and downs*, *wear and tear*,
  *odds and ends*, *peace and quiet*, *bits and pieces*, *now and then*, *sooner or later*.
- They sound very natural in speech and are quick wins for the vocabulary mark.
""", None),
            ("Organising Your Answer", [r"organi[sz](e|ing|ation)", r"structure (your|an|the) answer", r"\bfirstly\b", r"\bsecondly\b", r"\bto sum up\b", r"\bon the one hand\b", r"\bin conclusion\b", r"\bparagraph"], "Structuring a long turn, a monologue or an essay so the examiner can follow you.", """
**Discourse management** is a speaking criterion of its own: examiners check whether your answer has
a beginning, a middle and an end and whether ideas are linked.

- Start with a direct answer, give a reason, add an example, round off (*so, all in all…*).
- Signposts: *firstly / to begin with*, *another point is*, *on the one hand… on the other hand*,
  *having said that*, *to sum up*, *in conclusion*.
- In writing: one idea per paragraph, topic sentences, a clear conclusion.
""", None),
            ("Slang & Informal English", [r"\bslang\b", r"informal", r"colloquial", r"\bgonna\b", r"\bwanna\b", r"\bgrand\b", r"\bmate\b", r"\bcheers\b", r"\bbloke\b", r"\bdodgy\b"], "Gonna, grand, mate, dodgy – the informal English you hear from native speakers.", """
Native speakers use **informal English** constantly; you need to understand it for the listening
paper and to know when **not** to use it (formal essays, reports, letters of application).

- Irish: *grand* (fine), *craic* (fun), *yer man*, *deadly* (great). British: *mate*, *cheers*,
  *knackered*, *dodgy*, *quid*. American: *awesome*, *bucks*, *gonna*, *you guys*.
- *Gonna / wanna / gotta* are fine in speech, never in writing.
""", 4),
            ("Spelling", [r"\bspelling\b", r"\bspelt\b", r"\bspelled\b", r"\bhow do you spell\b", r"british spelling", r"american spelling", r"\bdouble (the )?(l|consonant)\b"], "British vs. American spelling and the words everyone misspells.", """
- **British vs. American**: *colour / color*, *centre / center*, *organise / organize* (both OK in
  the UK), *travelling / traveling*, *programme / program*.
- Frequent errors: *definitely*, *separate*, *necessary*, *accommodation*, *occurred*,
  *receive*, *which / witch*, *beginning*.
- Cambridge accepts either British or American spelling as long as it is consistent.
""", None),
            ("Verbs with Many Meanings (get, do, make, take)", [r"\b(the verb|uses of|ways to use) (get|do|make|take)\b", r"\bget\b.*\bmeanings?\b", r"\bmake or do\b", r"\bdo or make\b"], "The all-purpose verbs get, do, make and take and their many uses.", """
- **get**: receive (*get a letter*), become (*get tired*), arrive (*get home*), fetch (*get a drink*),
  understand (*I get it*), plus dozens of phrasal verbs (*get on, get over, get by, get away with*).
- **make vs. do**: *make* creates or decides (*make a cake, make a decision, make progress*);
  *do* performs (*do homework, do the dishes, do your best*).
- **take**: *take a photo, take part, take place, take advantage of, take it easy*.
""", None),
        ]
    ],
    # ------------------------------------------------------------------ Exams & skills
    *[
        {"name": n, "folder": "Exams", "patterns": p, "summary": s, "body": b, **({"min": m} if m else {})}
        for n, p, s, b, m in [
            ("Cambridge B2 First (FCE)", [r"B2 First", r"\bFCE\b", r"First Certificate", r"\bB2\b", r"First for Schools"], "The upper-intermediate Cambridge exam, formerly the First Certificate (FCE).", """
**B2 First** (formerly FCE) certifies upper-intermediate English. Four papers: Reading and Use of
English (75 min), Writing (80 min: essay + one of article, email/letter, report, review, story
*for Schools*), Listening (40 min) and Speaking (14 min, in pairs).

- Speaking: Part 1 interview, Part 2 long turn with two photos (1 minute), Part 3 collaborative
  task, Part 4 discussion.
- Pass marks: 160–179 = B2, 180+ = C1 on the Cambridge scale.
""", None),
            ("Cambridge C1 Advanced (CAE)", [r"C1 Advanced", r"\bCAE\b", r"\bC1\b", r"Certificate in Advanced English"], "The Cambridge exam most universities and employers ask for.", """
**C1 Advanced** (formerly CAE) proves you can follow academic study and professional life in English.
Papers: Reading and Use of English (90 min), Writing (90 min: essay + one of letter, proposal,
report, review), Listening (40 min), Speaking (15 min).

- Use of English Parts 1–4 test collocations, word formation and key-word transformations.
- Speaking Part 2: three pictures, talk about two for one minute; Part 3: a written prompt to discuss.
- Scale: 180–199 = C1, 200+ = C2.
""", None),
            ("Cambridge C2 Proficiency (CPE)", [r"C2 Proficiency", r"\bCPE\b", r"\bC2\b", r"Proficiency"], "The highest Cambridge level – near-native command of English.", """
**C2 Proficiency** (formerly CPE) is the top Cambridge qualification. Papers: Reading and Use of
English (90 min), Writing (90 min: discursive essay summarising two texts + one of article, letter,
report, review, or a set-text question), Listening (40 min), Speaking (16 min).

- Expect idiomatic language, inversion, cleft sentences and precise collocations throughout.
- The essay demands summarising and evaluating two short texts in your own words.
""", None),
            ("IELTS", [r"\bIELTS\b", r"\bband (score|7|8|9)\b"], "The International English Language Testing System, scored in bands from 1 to 9.", """
**IELTS** (Academic or General Training) is scored in **bands** 1–9; universities usually ask for
6.5–7.5. Papers: Listening (30 min), Reading (60 min), Writing (60 min: Task 1 graph/letter,
Task 2 essay) and a one-to-one Speaking interview (11–14 min, three parts).

- Unlike Cambridge exams you cannot fail; the band shows your level.
- Speaking Part 2 is a two-minute talk from a cue card after one minute of preparation.
""", None),
            ("Other Exams (TOEFL, Trinity, Aptis, EOI)", [r"\bTOEFL\b", r"\bTrinity\b", r"\bAptis\b", r"\bEOI\b", r"Escuela Oficial", r"\bLinguaskill\b", r"\bTOEIC\b"], "TOEFL, Trinity, Aptis, Linguaskill and the Spanish Escuela Oficial de Idiomas.", """
- **TOEFL iBT**: American, computer-based, scored out of 120; favoured by US universities.
- **Trinity ISE/GESE**: British exams with a strong oral component, popular in Spain and Italy.
- **Aptis** (British Council) and **Linguaskill** (Cambridge): quick online placement tests.
- **EOI** (Escuela Oficial de Idiomas): Spain's state language schools with their own B2/C1/C2 exams,
  which many of the podcast's listeners sit.
""", None),
            ("Speaking Exam", [r"speaking (exam|test|paper|part)", r"\boral exam\b", r"\bexaminer", r"\binterlocutor\b", r"\blong turn\b", r"\bcollaborative task\b", r"\bspeaking skills\b"], "How the speaking test works and what examiners are really listening for.", """
Cambridge speaking tests are marked on **Grammar and Vocabulary**, **Discourse Management**,
**Pronunciation** and **Interactive Communication** (plus a global mark from the interlocutor).

- Don't rehearse answers – examiners spot memorised speeches and they rarely fit the question.
- Interact: react to your partner, ask their opinion, agree and disagree politely.
- Keep going: if you run out of ideas, paraphrase, give an example, speculate.
- Fillers that buy time: *That's an interesting question…*, *Let me think…*, *Well, I suppose…*
""", None),
            ("Writing Exam", [r"writing (exam|paper|part|task|test)", r"\bessays?\b", r"\bformal letter\b", r"\binformal letter\b", r"\breport\b", r"\bproposal\b", r"\breview\b", r"\barticle\b", r"\bwriting skills\b"], "Essays, letters, reports, reviews and articles – what each task needs.", """
Cambridge writing is marked on **Content**, **Communicative Achievement**, **Organisation** and
**Language**. Each task type has its own conventions:

- **Essay**: formal, balanced, clear paragraphs, a conclusion with your view.
- **Letter/email**: match the register to the reader; formal letters open *Dear Sir/Madam* and close
  *Yours faithfully*.
- **Report/proposal**: headings, neutral tone, recommendations.
- **Review/article**: engaging title, personal voice, a recommendation at the end.
- Use the word limit, plan for five minutes, leave time to check.
""", None),
            ("Listening & Reading", [r"listening (exam|paper|part|skills|practice)", r"reading (paper|part|skills)", r"use of english", r"\bkey word transformation", r"\bmultiple choice\b", r"\bgapped text\b"], "Listening practice with different accents and the Reading & Use of English paper.", """
- **Listening**: Cambridge recordings mix British, Irish, American, Australian and other accents –
  exactly what this podcast trains. Read the questions first, listen for paraphrase, never leave a
  blank.
- **Reading and Use of English**: multiple-choice cloze (collocations), open cloze (grammar words),
  word formation, key-word transformations, then reading tasks (multiple choice, gapped text,
  multiple matching).
""", None),
            ("Exam Tips & Preparation", [r"exam (tips?|preparation|day|advice|strateg)", r"\btop tip", r"\bprepar(e|ing) for (the|your|an) exam", r"\brevis(e|ion)\b", r"\bnervous\b", r"\bpractice (makes|test)", r"\bexam technique"], "Practical advice for the weeks before the exam and for the day itself.", """
- Practise with past papers under timed conditions; know the task formats inside out.
- Build vocabulary by topic and record whole phrases, not single words.
- Listen to a wide range of accents (podcasts, series, radio) every day.
- On the day: read instructions twice, manage your time, and in the speaking test treat the examiner
  and your partner as people you are chatting to – nerves fade once you start talking.
""", None),
        ]
    ],
    # ------------------------------------------------------------------ Accents (where the speakers come from)
    *[
        {"name": n, "folder": "Accents", "patterns": p, "summary": s, "body": b, "min": 2}
        for n, p, s, b in [
            ("Ireland", [r"\bIreland\b", r"\bIrish\b", r"\bDublin\b", r"\bCork\b", r"\bLimerick\b", r"\bGalway\b", r"\bBelfast\b"], "Trevor's home: Irish English, its sounds and its slang.", """
**Irish English** is the podcast's home accent (Trevor is from Ireland). Features: a soft *r* that is
always pronounced, *th* often sounding close to *t/d* (*tree* for *three*), rising intonation, and a
vocabulary of its own: *grand* (fine), *craic* (fun, good atmosphere), *yer man* (that guy),
*deadly* (great), *to give out* (to scold), *press* (cupboard).
"""),
            ("England", [r"\bEngland\b", r"\bBritish\b", r"\bLondon\b", r"\bManchester\b", r"\bLiverpool\b", r"\bChester\b", r"\bYorkshire\b", r"\bEnglish accent\b", r"\bRP\b", r"\bcockney\b", r"\bBrits?\b"], "British English from London to the North – RP, Estuary, Northern and more.", """
England has dozens of accents: **RP / BBC English**, Estuary (London area), Cockney, Northern
accents (Manchester, Liverpool *Scouse*, Yorkshire, Geordie in Newcastle). Shared features: the
non-rhotic *r* (*car* → /kɑː/), the long /ɑː/ in *bath, dance* in the South, the short /æ/ in the
North, and *t*-glottalling (*butter* → "bu'er") in informal speech. Vocabulary: *mate*, *cheers*,
*quid*, *loo*, *fortnight*, *knackered*.
"""),
            ("Scotland", [r"\bScotland\b", r"\bScottish\b", r"\bGlasgow\b", r"\bEdinburgh\b", r"\bScots\b"], "Scottish English – rolled r, wee and aye.", """
**Scottish English** keeps the rolled or tapped *r*, has distinct vowels (*house* sounds closer to
*hoose* in broad accents) and its own words: *wee* (small), *aye* (yes), *bonnie* (pretty),
*loch* (lake), *ken* (know), *dreich* (grey, miserable weather). Glasgow and Edinburgh accents differ
noticeably.
"""),
            ("Wales", [r"\bWales\b", r"\bWelsh\b", r"\bCardiff\b", r"\bSwansea\b"], "Welsh English with its musical, sing-song intonation.", """
**Welsh English** is known for its rising-and-falling, musical intonation and for sentence patterns
influenced by the Welsh language (*I do go there every week*, *there's lovely*). Vocabulary: *tidy*
(good), *cwtch* (a cuddle), *now in a minute* (soon), *lush* (great).
"""),
            ("USA", [r"\bUSA\b", r"(?-i:\bUS\b)", r"United States", r"\bAmerican?\b", r"\bNew York\b", r"\bTexas\b", r"\bCalifornia\b", r"\bBoston\b", r"\bPennsylvania\b", r"\bNew Hampshire\b", r"\bChicago\b"], "American English – rhotic r, flapped t and its own vocabulary.", """
**American English** is rhotic (*car* with a clear *r*), turns *t* between vowels into a quick *d*
sound (*water* → "wadder") and uses different words: *apartment, elevator, vacation, candy, cookie,
sidewalk, trash, fall (autumn)*. Regional accents range from Boston and New York to the Southern
drawl of Texas. Spelling: *color, center, organize, traveling*.
"""),
            ("Canada", [r"\bCanada\b", r"\bCanadian\b", r"\bToronto\b", r"\bVancouver\b", r"\bMontreal\b"], "Canadian English – close to American, with British spelling and 'eh'.", """
**Canadian English** sounds close to General American but keeps some British spellings (*colour,
centre*) and vocabulary (*washroom, toque, loonie*). *Canadian raising* makes *about* sound
(to American ears) like "aboot". *Eh?* at the end of a sentence works like a question tag.
"""),
            ("Australia", [r"\bAustralia\b", r"\bAustralian\b", r"\bAussie\b", r"\bSydney\b", r"\bMelbourne\b", r"\bBrisbane\b", r"\bPerth\b"], "Australian English – shortened words, rising intonation and plenty of slang.", """
**Australian English** is non-rhotic, with a rising intonation at the end of statements (*high rising
terminal*) and a love of shortened words: *arvo* (afternoon), *brekkie* (breakfast), *barbie*
(barbecue), *servo* (petrol station), *mozzie*, *sunnies*. *Mate*, *no worries*, *reckon* and *heaps*
(a lot) are everyday words.
"""),
            ("New Zealand", [r"\bNew Zealand\b", r"\bKiwi\b", r"\bAuckland\b", r"\bWellington\b", r"(?-i:\bNZ\b)"], "New Zealand English – the shifted vowels that make 'fish and chips' sound like 'fush and chups'.", """
**New Zealand English** resembles Australian but with centralised short vowels: *six* sounds like
*sucks* to outsiders, *bed* like *bid*. Māori loanwords are common (*kia ora* – hello, *whānau* –
family, *kai* – food). Slang: *sweet as* (great), *chur* (thanks), *jandals* (flip-flops), *dairy*
(corner shop).
"""),
            ("South Africa", [r"\bSouth Africa\b", r"\bSouth African\b", r"\bCape Town\b", r"\bJohannesburg\b", r"\bDurban\b"], "South African English, shaped by Afrikaans and Zulu.", """
**South African English** has clipped vowels (*yes* → "yis"), a *kit–bit* split and borrowings from
Afrikaans and African languages: *lekker* (nice), *braai* (barbecue), *robot* (traffic light),
*now now* (soon), *shame* (expressing sympathy), *howzit* (hello). It is one of eleven official
languages in the country.
"""),
            ("Non-Native Speakers", [r"non-native", r"\bSpanish\b", r"\bSpain\b", r"\bPoland\b", r"\bPolish\b", r"\bBrazil", r"\bVietnam", r"\bChina\b", r"\bChinese\b", r"\bItalian\b", r"\bItaly\b", r"\bGerman\b", r"\bFrench\b", r"\bTokyo\b", r"\bBarcelona\b"], "Learners and non-native teachers who speak in the podcast – and the countries they come from.", """
Several episodes feature **non-native speakers** – students and teachers from Spain, Poland,
Brazil, Vietnam and China – talking about their own path to fluent English. Their experiences are
especially relatable: typical mistakes of their first language, the role of living abroad, and whether
a non-native teacher has advantages. Trevor himself teaches in Spain, so Spanish learners are the
podcast's biggest audience.
"""),
        ]
    ],
]
