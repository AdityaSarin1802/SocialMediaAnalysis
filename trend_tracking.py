"""
Trend Tracking Module
----------------------
Uses TF-IDF to find the keywords/phrases that best characterize the
current batch of posts, plus simple frequency counts to show which
topics are gaining volume.

For production: replace with a streaming topic model (BERTopic) and
compare keyword volume across time windows to detect real "bursts".
"""

from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

STOPWORDS = {
    "the", "is", "in", "at", "of", "a", "an", "to", "and", "for", "on",
    "this", "that", "it", "are", "was", "were", "be", "our", "my", "i",
    "we", "you", "everyone", "will", "with", "has", "have", "hai", "ki",
    "ka", "ko", "bahut", "hoga"
}


def extract_top_keywords(posts: list, top_n: int = 5) -> list:
    """Return the top N TF-IDF weighted keywords across all posts."""
    texts = [p["text"] for p in posts]
    if not texts:
        return []

    vectorizer = TfidfVectorizer(stop_words=list(STOPWORDS), ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(texts)
    scores = matrix.sum(axis=0).A1
    terms = vectorizer.get_feature_names_out()

    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return [{"term": term, "score": round(float(score), 3)} for term, score in ranked[:top_n]]


def topic_volume_over_time(posts: list, keyword: str) -> dict:
    """Count how many posts mentioning `keyword` fall on each date."""
    counts = Counter()
    for p in posts:
        if keyword.lower() in p.get("text", "").lower():
            date = p.get("timestamp", "unknown").split("T")[0]
            counts[date] += 1
    return dict(sorted(counts.items()))


def detect_trending_topics(posts: list, top_n: int = 3) -> list:
    """
    Cluster posts loosely by shared top keyword, and report volume +
    day-over-day growth for each — a simple stand-in for burst detection.
    """
    keywords = extract_top_keywords(posts, top_n=top_n)
    trends = []
    for kw in keywords:
        term = kw["term"]
        volume_by_day = topic_volume_over_time(posts, term)
        total_volume = sum(volume_by_day.values())
        trends.append({
            "topic": term,
            "tfidf_score": kw["score"],
            "total_mentions": total_volume,
            "volume_by_day": volume_by_day,
        })
    return trends