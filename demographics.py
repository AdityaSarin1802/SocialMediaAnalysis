"""
Demographics Module
---------------------
IMPORTANT (say this to jurors): real demographic inference must only
use public, aggregate, non-PII signals (declared profile language,
public location tag, posting-pattern clustering) - never private data.

For this prototype, posts already carry `region` / `language` tags to
simulate the output of an upstream inference step, and this module
just aggregates them. In production, this would be a proper
classifier trained on public metadata + linguistic signals.
"""

from collections import Counter


def demographic_breakdown(posts: list) -> dict:
    regions = Counter(p.get("region", "unknown") for p in posts)
    languages = Counter(p.get("language", "unknown") for p in posts)
    return {
        "by_region": dict(regions),
        "by_language": dict(languages),
        "total_posts": len(posts),
    }


def demographic_sentiment_crosstab(enriched_posts: list) -> dict:
    """
    Cross-reference region with sentiment label - this is the kind of
    fused insight ("which region is turning negative") that's the
    whole point of the project.
    """
    crosstab = {}
    for post in enriched_posts:
        region = post.get("region", "unknown")
        label = post["sentiment"]["label"]
        crosstab.setdefault(region, {"positive": 0, "negative": 0, "neutral": 0})
        crosstab[region][label] += 1
    return crosstab