"""
Sentiment Analysis Module
--------------------------
Lexicon-based sentiment scoring (works fully offline - no large model
downloads needed for a hackathon demo).

For the production version, swap `score_text()` internals with a
fine-tuned transformer (e.g. IndicBERT / XLM-RoBERTa) to properly
handle regional languages and code-mixed text (Hinglish etc).
"""

import re

POSITIVE_WORDS = {
    "good", "great", "excellent", "promising", "thank", "thanks", "relieved",
    "happy", "excited", "finally", "responding", "hope", "hoping", "positive",
    "accha", "welcome", "improve", "improving", "support", "resolved"
}

NEGATIVE_WORDS = {
    "shortage", "crisis", "bad", "terrifying", "scary", "panicking", "rumors",
    "worried", "worse", "worsen", "stress", "rushed", "overwhelmed", "kami",
    "problem", "fail", "failed", "angry", "unfair", "complaint", "complaints"
}

NEGATION_WORDS = {"not", "no", "never", "nahi", "won't", "don't", "doesn't"}


def _tokenize(text: str):
    return re.findall(r"[a-zA-Z']+", text.lower())


def score_text(text: str) -> dict:
    """Return a sentiment label + numeric polarity score for one post."""
    tokens = _tokenize(text)
    pos_hits, neg_hits = 0, 0

    for i, tok in enumerate(tokens):
        negated = i > 0 and tokens[i - 1] in NEGATION_WORDS
        if tok in POSITIVE_WORDS:
            neg_hits += 1 if negated else 0
            pos_hits += 0 if negated else 1
        elif tok in NEGATIVE_WORDS:
            pos_hits += 1 if negated else 0
            neg_hits += 0 if negated else 1

    score = pos_hits - neg_hits
    if score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"
    else:
        label = "neutral"

    return {"label": label, "score": score, "pos_hits": pos_hits, "neg_hits": neg_hits}


def analyze_posts(posts: list) -> list:
    """Attach sentiment results to each post dict."""
    enriched = []
    for post in posts:
        result = score_text(post["text"])
        enriched.append({**post, "sentiment": result})
    return enriched


def sentiment_distribution(enriched_posts: list) -> dict:
    """Aggregate counts of each sentiment label."""
    dist = {"positive": 0, "negative": 0, "neutral": 0}
    for post in enriched_posts:
        dist[post["sentiment"]["label"]] += 1
    return dist