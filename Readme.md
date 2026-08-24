SIH 26152 — Social Media Analytics Framework (NTRO)
Prototype backend demonstrating the four-vector fusion concept: **Sentiment
Demographics + Trend Tracking + Network Analysis → one unified insight
report.**
Why these choices
Flask — simplest way to stand up a REST API fast for a hackathon demo.
Lexicon-based sentiment (modules/sentiment_analysis.py) — works
fully offline, no model download needed for the demo. Swap in a
fine-tuned transformer (IndicBERT / XLM-RoBERTa) for production-grade
accuracy and regional-language support.
TF-IDF trend extraction (modules/trend_tracking.py, via
scikit-learn) — lightweight stand-in for a full topic model (BERTopic)
in production.
NetworkX (modules/network_analysis.py) — builds the mentions graph
and ranks influencers via PageRank + in-degree centrality, detects
communities via greedy modularity. Swap for Neo4j at scale.
modules/demographics.py — aggregates region/language tags. In this
prototype those tags are provided directly in the mock data to simulate
the output of an upstream inference step; a real system would infer
these from public, non-PII signals only.
modules/fusion.py — the actual differentiator: cross-references
sentiment against region to auto-generate analyst alerts like
"Region X is trending negative."
Setup
Bash
Server runs at http://127.0.0.1:5000.
Try it
Bash
Or run the included test script, which exercises every endpoint:
Bash
Endpoints
Method
Route
Description
GET
/
Health check + endpoint list
GET
/api/posts
Raw ingested posts
POST
/api/ingest
Add a new post (demo of live ingestion)
GET
/api/sentiment
Per-post + aggregate sentiment
GET
/api/trends
Top trending topics (TF-IDF + volume)
GET
/api/network
Top influencers + detected communities
GET
/api/demographics
Region/language breakdown
GET
/api/fusion
The combined report — lead with this in your demo
Team mapping suggestion
Each module maps to one presentation owner from your team of 6:
sentiment_analysis.py, demographics.py, trend_tracking.py,
network_analysis.py, fusion.py + app.py, plus one member owning
architecture/Q&A framing.
Next steps for production
Replace lexicon sentiment with a fine-tuned transformer.
Replace mock data with real platform API ingestion (rate-limited,
consent-respecting).
Move the graph to Neo4j for scale.
Add a streaming layer (Kafka) for real-time alerting.
Deploy on-premise/air-gapped infrastructure given the NTRO context.