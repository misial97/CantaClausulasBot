import sqlite3, hashlib, time
from contextlib import closing

DB_PATH = "seen.db"

def ensure_db():
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS seen(
                id TEXT PRIMARY KEY,
                event_ts INTEGER NOT NULL,     -- epoch del movimiento
                first_seen_ts INTEGER NOT NULL -- epoch cuándo lo vimos
            )
        """)
        con.commit()

def event_id_for(*parts: str) -> str:
    """Crea un ID estable (hash) a partir de buyer, seller, player, amount, date."""
    key = "||".join(map(str, parts))
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def is_seen(eid: str) -> bool:
    with closing(sqlite3.connect(DB_PATH)) as con:
        cur = con.execute("SELECT 1 FROM seen WHERE id=?", (eid,))
        return cur.fetchone() is not None

def mark_seen(eid: str, event_ts: int):
    now = int(time.time())
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute("INSERT OR IGNORE INTO seen(id, event_ts, first_seen_ts) VALUES (?,?,?)",
                    (eid, int(event_ts), now))
        con.commit()