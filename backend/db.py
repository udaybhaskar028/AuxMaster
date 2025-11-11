# backend/db.py
from pathlib import Path
from sqlalchemy import create_engine, text

DB_PATH = Path(__file__).parent / "auxmaster.db"

# Lazily create the engine so importing this module never fails
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        # echo=False keeps logs quiet; SQLite file lives in /backend/
        _engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
    return _engine

def init_db():
    """Create the feedback table if it doesn't exist."""
    eng = get_engine()
    with eng.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER NOT NULL,
            liked INTEGER NOT NULL,         -- 1 like, 0 dislike
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """))
