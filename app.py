"""
SIH 26152 - Social Media Analytics for NTRO
Prototype Backend (Flask)
=============================================
Run with:  python app.py
Then visit: http://127.0.0.1:5000/

Endpoints:
  GET  /                      -> health check + endpoint list
  GET  /api/posts             -> raw ingested posts
  POST /api/ingest            -> add a new post (demo of live ingestion)
  GET  /api/sentiment         -> sentiment analysis results
  GET  /api/trends            -> trending topics
  GET  /api/network           -> influencer + community graph analysis
  GET  /api/demographics      -> demographic breakdown
  GET  /api/fusion            -> the combined, unified intelligence report
"""

import json
import os
from flask import Flask, jsonify, request

from modules import sentiment_analysis, trend_tracking, network_analysis, demographics, fusion

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_posts.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    POSTS = json.load(f)


@app.route("/")
def index():
    return jsonify({
        "project": "SIH 26152 - Social Media Analytics Framework (NTRO)",
        "status": "running",
        "loaded_posts": len(POSTS),
        "endpoints": [
            "/api/posts", "/api/ingest [POST]", "/api/sentiment",
            "/api/trends", "/api/network", "/api/demographics", "/api/fusion",
        ],
    })


@app.route("/api/posts")
def get_posts():
    return jsonify(POSTS)


@app.route("/api/ingest", methods=["POST"])
def ingest_post():
    """Demo endpoint showing how new posts would be added in real time."""
    new_post = request.get_json(force=True)
    required = {"post_id", "user_id", "text"}
    if not required.issubset(new_post):
        return jsonify({"error": f"Missing required fields: {required}"}), 400
    import datetime
    new_post.setdefault("mentions", [])
    new_post.setdefault("region", "unknown")
    new_post.setdefault("language", "unknown")
    new_post.setdefault("timestamp", datetime.datetime.utcnow().isoformat())
    POSTS.append(new_post)
    return jsonify({"message": "Post ingested", "total_posts": len(POSTS)}), 201


@app.route("/api/sentiment")
def get_sentiment():
    enriched = sentiment_analysis.analyze_posts(POSTS)
    return jsonify({
        "distribution": sentiment_analysis.sentiment_distribution(enriched),
        "posts": enriched,
    })


@app.route("/api/trends")
def get_trends():
    top_n = int(request.args.get("top_n", 5))
    return jsonify(trend_tracking.detect_trending_topics(POSTS, top_n=top_n))