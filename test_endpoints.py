from app import app
import json

client = app.test_client()

for ep in ["/", "/api/posts", "/api/sentiment", "/api/trends",
           "/api/network", "/api/demographics", "/api/fusion"]:
    r = client.get(ep)
    print(ep, "->", r.status_code, len(r.data), "bytes")
    assert r.status_code == 200, "FAILED: " + ep

r = client.post("/api/ingest", json={"post_id": "p999", "user_id": "u1",
                                      "text": "test post about water shortage"})
print("POST /api/ingest ->", r.status_code, r.get_json())

fusion_resp = client.get("/api/fusion").get_json()
print()
print("=== FUSION SUMMARY ===")
print(json.dumps(fusion_resp["summary"], indent=2))
print()
print("=== ALERTS ===")
print(json.dumps(fusion_resp["alerts"], indent=2))
print()
print("ALL ENDPOINTS OK")