# backend/app.py

import os
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import bindparam, text

# IMPORTANT: absolute imports so Render doesn't get confused
from backend.model import ContentRecommender
from backend.db import engine, init_db

# -----------------------------------------------------------------------------
# ASGI app object (must be named 'app' at module top-level)
# -----------------------------------------------------------------------------
app = FastAPI(title="AuxMaster API", version="1.0")

# CORS
origins = os.getenv("AUXMASTER_CORS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB + model init
init_db()
recommender = ContentRecommender()

# -----------------------------------------------------------------------------
# Schemas
# -----------------------------------------------------------------------------
class RecommendRequest(BaseModel):
    query: str
    k: int = 10


class FeedbackRequest(BaseModel):
    track_id: int
    liked: bool


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend")
def recommend(req: RecommendRequest):
    results = recommender.recommend_by_title(req.query, top_k=req.k)
    if not results:
        raise HTTPException(status_code=404, detail="Song not found")

    ids = [int(r["id"]) for r in results]
    feedback_map = {}

    if ids:
        stmt = (
            text(
                "SELECT track_id, "
                "SUM(CASE liked WHEN 1 THEN 1 ELSE -1 END) AS score "
                "FROM feedback WHERE track_id IN :ids GROUP BY track_id"
            ).bindparams(bindparam("ids", expanding=True))
        )
        with engine.begin() as conn:
            rows = conn.execute(stmt, {"ids": ids}).mappings().all()
        feedback_map = {int(r["track_id"]): int(r["score"]) for r in rows}

    for r in results:
        bonus = feedback_map.get(int(r["id"]), 0)
        r["adjusted_score"] = float(round(r["score"] + 0.05 * bonus, 6))

    results.sort(key=lambda x: x["adjusted_score"], reverse=True)
    return {"results": results}


@app.post("/feedback")
def feedback(req: FeedbackRequest):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO feedback (track_id, liked) VALUES (:tid, :liked)"),
            {"tid": req.track_id, "liked": 1 if req.liked else 0},
        )
    return {"ok": True}
