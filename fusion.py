"""
Fusion Module
--------------
This is the core differentiator of the project: instead of reporting
sentiment, demographics, trends, and network structure separately,
this module combines them into single, analyst-readable insights,
e.g. "Region X is turning negative on Topic Y, amplified by Influencer Z".
"""

import sentiment_analysis, trend_tracking, network_analysis, demographics


def generate_fused_report(posts: list) -> dict:
    enriched_posts = sentiment_analysis.analyze_posts(posts)

    sentiment_dist = sentiment_analysis.sentiment_distribution(enriched_posts)
    trends = trend_tracking.detect_trending_topics(posts, top_n=3)
    network = network_analysis.graph_summary(posts, top_n=5)
    demo_breakdown = demographics.demographic_breakdown(posts)
    demo_sentiment = demographics.demographic_sentiment_crosstab(enriched_posts)

    # Flag the most concerning combination: a region trending negative
    alerts = []
    for region, counts in demo_sentiment.items():
        if counts["negative"] > counts["positive"] and counts["negative"] >= 2:
            alerts.append(
                f"Region '{region}' shows net-negative sentiment "
                f"({counts['negative']} negative vs {counts['positive']} positive posts) "
                f"— worth analyst review."
            )

    return {
        "summary": {
            "total_posts_analyzed": len(posts),
            "sentiment_distribution": sentiment_dist,
            "top_trending_topics": [t["topic"] for t in trends],
            "num_users_in_network": network["num_users"],
            "top_influencer": network["top_influencers"][0] if network["top_influencers"] else None,
        },
        "sentiment": sentiment_dist,
        "trends": trends,
        "network": network,
        "demographics": demo_breakdown,
        "demographic_sentiment_crosstab": demo_sentiment,
        "alerts": alerts,
    }