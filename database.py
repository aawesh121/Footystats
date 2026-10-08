"""SQLite helpers + schema. Used by app.py and scripts/load_data.py."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "players.db"

SCHEMA = """
DROP TABLE IF EXISTS performances;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
    player_id     INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    image_url     TEXT,
    date_of_birth TEXT,
    nationality   TEXT,
    position      TEXT,
    height        TEXT,
    foot          TEXT,
    current_club  TEXT,
    market_value  TEXT
);

CREATE TABLE performances (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id   INTEGER NOT NULL,
    season      TEXT,
    team        TEXT,
    competition TEXT,
    matches     INTEGER DEFAULT 0,
    goals       INTEGER DEFAULT 0,
    assists     INTEGER DEFAULT 0,
    minutes     INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players (player_id)
);

CREATE INDEX idx_players_name ON players (name);
CREATE INDEX idx_perf_player  ON performances (player_id);
"""


def get_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path=DB_PATH):
    conn = get_db(path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def search_players(query, limit=25, path=DB_PATH):
    conn = get_db(path)
    rows = conn.execute(
        "SELECT player_id, name, position, current_club, image_url "
        "FROM players WHERE name LIKE ? ORDER BY name LIMIT ?",
        (f"%{query}%", limit),
    ).fetchall()
    conn.close()
    return rows


def get_player(player_id, path=DB_PATH):
    conn = get_db(path)
    row = conn.execute("SELECT * FROM players WHERE player_id = ?", (player_id,)).fetchone()
    conn.close()
    return row


def get_performances(player_id, path=DB_PATH):
    conn = get_db(path)
    rows = conn.execute(
        "SELECT season, team, competition, matches, goals, assists, minutes "
        "FROM performances WHERE player_id = ? ORDER BY season, competition",
        (player_id,),
    ).fetchall()
    conn.close()
    return rows
