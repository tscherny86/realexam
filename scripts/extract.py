"""Pulls two things out of a transcript that the podcast makes explicit:

- the expressions Trevor picks out ("this phrasal verb to put off means…", "we had the expression a blast from the
  past") → vocabulary of the episode, each with the minute it is explained at
- the exam questions that are asked ("What kind of art do you enjoy?") → a question bank with the minute the
  native speakers' answers start

Both work on the final word list (after alignment and corrections). Used by build_wiki.py.
"""
import re

KINDS = r"(?:phrasal verb|expression|idiom|word|collocation|adjective|adverb|noun|verb|phrase|structure|saying|connector|binomial|compound adjective)"
LEAD = r"(?:the|this|that|another|a|an|one|our first|our second|the next|the first|the last|the second|the third) (?:really |very |super |lovely |nice |great |good |useful |brilliant |fantastic |classic |common |little |interesting )*" + KINDS + r"s?"
STOP = re.compile(r"^(?:is|was|that|which|here|there|the|a|an|to|of|in|and|it|this|again|also|then|so|you|we|they|he|she|i|very|really|quite|just|like|something|someone)$", re.I)
TERM = r"([A-Za-z][A-Za-z'’ -]{2,45}?)"
PATTERNS = [
    # "the phrasal verb to put off means" / "this expression, to buy time, is"
    re.compile(LEAD + r"[,:]? (?:here |there |again |in the answer )?(?:was |is |here is |here was |which was |which is |)(?:to )?" + TERM + r"(?=,|\.|;| which| that| and| –| -| means| meaning| is | was | here| so )", re.I),
    # "we had the expression X" / "we also heard X, which means"
    re.compile(r"\b(?:we (?:also )?(?:had|heard|have)|there was|there's|there is) (?:this |the |a |an |another |one )?(?:really |nice |lovely |great |super |useful |good |brilliant )*" + KINDS + r"s? (?:here |there |again |in there )?(?:which was |which is |, |:? )?(?:to )?" + TERM + r"(?=,|\.|;| which| that| and| –| -| means| meaning)", re.I),
    # "to X means" / "X, which means"
    re.compile(r"\b(?:so |and |okay, |now, )?to " + TERM + r" means\b", re.I),
    re.compile(r"\b(?:so |and )?" + TERM + r", which (?:basically |essentially |just )?means\b", re.I),
]
QUESTION = re.compile(
    r"\b((?:Do|Does|Did|What|Which|How|Why|Where|When|Who|Is|Are|Was|Were|Would|Should|Could|Can|Have|Has|Tell (?:us|me)|Describe|In your opinion|Some people say)\b[^.!?]{12,160}\?)",
    re.I,
)
BAD_QUESTION = re.compile(r"\b(you know|right|okay|isn't it|innit|remember|guys|listeners?|transcripts?|website|podcast|episode|examiner|exam|Trevor|I mean|did you hear|what did (?:he|she|they) say|what does (?:that|this|it) mean|which means|haven't you|what's the|how do you spell|what did we|what have we|what else)\b", re.I)
GOOD_START = re.compile(r"^(?:Do you|Does |Did you|What |Which |How |Why |Where |When |Who |Is |Are |Was |Were |Would you|Should |Could you|Can you|Have you|Has |Tell (?:us|me)|Describe |In your opinion|Some people say)", re.I)


BAD_START = re.compile(r"^(?:but|that|while|which|in|for|with|has|have|is|was|we|you|it|they|he|she|i|and|or|so|of|on|at|by|as|if|because|when|where|very|really|quite|just|here|there|these|those|this|again|also|then|some|any|all|one|two|not|no|yes|okay|ok|like|use|used|using|know|going|getting|too|lot|age|normally|relating|describe|talk|give|interrupt|favourite|long|thing|what|acquired|be or)\b", re.I)
BAD_END = re.compile(r"\b(?:which|that|and|or|but|too|again|kinda|sort|kind|like|the|a|an|of|in|so|very|really|then|before|right|just|new|is|it|correctly|politely|exams?|business)$", re.I)
COMMON = {"have", "well", "set", "form", "track", "smart", "sick", "broad", "regular", "before", "electricity", "clothe", "pay", "money", "parent", "parents", "people", "thing", "things", "good", "bad", "nice", "like", "time", "work", "say", "said", "get", "go", "make", "know", "think", "want", "use", "used", "word", "words", "one", "way", "lot", "bit", "today", "too", "rock", "sights", "ache"}
EXPLAIN = re.compile(r"\b(?:means|meaning|which is|is used|we use|you use|is another way|is a way|is when|refers to|describes|the opposite of|synonym)\b", re.I)
PHRASE_KINDS = {"phrasal verb", "idiom", "expression", "collocation", "binomial", "compound adjective", "saying", "connector"}


def _clean_term(t: str) -> str | None:
    t = re.sub(r"\s+", " ", t.strip(" ,.;:'’\"-"))
    t = re.sub(r"^(?:to |the |a |an |my |your |his |her )+", "", t, flags=re.I).strip()
    words = t.split()
    if not 1 <= len(words) <= 4 or len(t) < 3:
        return None
    if STOP.match(t) or all(STOP.match(w) for w in words) or BAD_START.match(t) or BAD_END.search(t):
        return None
    if re.search(r"\b(?:means|meaning|example|answer|question|speaker|transcript|episode|exam|examiner|heard|said|here|there|again|these|those|I'm|I’m|would|past participle|hyphen|phrasal|verbs?|nouns?|adjectives?|figurative|Cambridge|IELTS)\b", t, re.I):
        return None
    if len(words) == 1 and t.lower() in COMMON:
        return None
    if t.isupper():
        return t.lower()
    if t[0].isupper() and not re.match(r"^[A-Z][a-z]+ [A-Z]", t):
        t = t[0].lower() + t[1:]
    return t


def sentences(words: list[dict]):
    """Yields (text, start) per sentence."""
    buf = []
    for w in words:
        buf.append(w)
        if re.search(r"[.!?]['\"”’]?$", w["text"]):
            yield " ".join(x["text"] for x in buf), buf[0]["start"]
            buf = []
    if buf:
        yield " ".join(x["text"] for x in buf), buf[0]["start"]


def vocabulary(words: list[dict], limit: int = 25) -> list[dict]:
    """-> [{"term": "put off", "t": 123.4, "kind": "phrasal verb"}] in order of appearance, deduplicated."""
    out, seen = [], set()
    for text, start in sentences(words):
        if not re.search(KINDS + r"|means\b", text, re.I):
            continue
        for rx in PATTERNS:
            for m in rx.finditer(text):
                term = _clean_term(m.group(1))
                if not term:
                    continue
                key = re.sub(r"[^a-z]", "", term.lower())
                if key in seen:
                    continue
                kind = re.search(KINDS, m.group(0), re.I)
                kind = kind.group(0).lower() if kind else "expression"
                # single words and plain "word/adjective/verb" finds only count when the sentence explains them
                if (kind not in PHRASE_KINDS or len(term.split()) == 1) and not EXPLAIN.search(text):
                    continue
                seen.add(key)
                out.append({"term": term, "t": round(start, 2), "kind": kind})
    return out[:limit]


def questions(words: list[dict], limit: int = 12) -> list[dict]:
    """-> [{"q": "What kind of art do you enjoy?", "t": 45.1}] – the exam-style questions asked in the episode."""
    out, seen = [], set()
    for text, start in sentences(words):
        if not text.rstrip().endswith("?"):
            continue
        m = QUESTION.search(text)
        if not m:
            continue
        q = m.group(1).strip()
        q = q[0].upper() + q[1:]
        n = len(q.split())
        if not 6 <= n <= 28 or not GOOD_START.match(q) or BAD_QUESTION.search(q):
            continue
        if re.search(r"\b(?:I|me|my|myself)\b", q):  # exam questions address "you"; first-person echoes are the answer
            continue
        if re.search(r"\blike,|, like\b|\bI mean\b|\byou know\b|\bum\b|\buh\b|\bsort of\b|\bkind of\b", q) or re.match(r"^(?:Is|Was|Are|Were) (?:how|what|like|it the)\b", q):
            continue
        # the speaker often repeats the question in the first person ("Who do I look up to?") – same question
        key = re.sub(r"\b(?:i|me|my|myself|mine)\b", "you", q.lower()).replace("your", "you")
        key = re.sub(r"\b(?:do|does|did|usually|generally|that)\b", "", key)
        key = re.sub(r"[^a-z]", "", key)
        if key in seen:
            continue
        seen.add(key)
        out.append({"q": q, "t": round(start, 2)})
    return out[:limit]
