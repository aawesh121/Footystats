"""Load the two CSV files into SQLite.

Usage:
    python scripts/load_data.py
Put player_profiles.csv and player_performances.csv in data/ first.
Column names differ between dataset versions, so each field below lists
candidate names; the first one found is used. Run with --inspect to see columns.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import database  # noqa: E402

DATA = ROOT / "data"

PROFILE_MAP = {
    "player_id": ["player_id"],
    "name": ["player_name", "name"],
    "image_url": ["player_image_url", "image_url"],
    "date_of_birth": ["date_of_birth"],
    "nationality": ["citizenship", "country_of_citizenship", "nationality"],
    "position": ["position", "main_position"],
    "height": ["height", "height_in_cm"],
    "foot": ["foot"],
    "current_club": ["current_club_name", "current_club"],
    "market_value": ["current_market_value", "market_value_in_eur", "market_value"],
}

PERF_MAP = {
    "player_id": ["player_id"],
    "season": ["season_name", "season"],
    "team": ["team_name", "team", "club_name"],
    "competition": ["competition_name", "competition"],
    "matches": ["nb_on_pitch", "appearances", "matches", "games"],
    "goals": ["goals"],
    "assists": ["assists"],
    "minutes": ["minutes_played", "minutes"],
}


def pick(df, mapping):
    """Return a new DataFrame with our column names; missing columns become None."""
    out = pd.DataFrame()
    for ours, candidates in mapping.items():
        found = next((c for c in candidates if c in df.columns), None)
        out[ours] = df[found] if found else None
        if not found:
            print(f"  ! no column found for '{ours}' (tried {candidates})")
    return out


def main():
    profiles_csv = DATA / "player_profiles.csv"
    perf_csv = DATA / "player_performances.csv"
    for f in (profiles_csv, perf_csv):
        if not f.exists():
            sys.exit(f"Missing {f}. Copy the CSV files into data/ first.")

    profiles = pd.read_csv(profiles_csv)
    perf = pd.read_csv(perf_csv)

    if "--inspect" in sys.argv:
        print("profiles:", list(profiles.columns))
        print("performances:", list(perf.columns))
        return

    players = pick(profiles, PROFILE_MAP).dropna(subset=["player_id", "name"])
    players = players.drop_duplicates("player_id")
    players["player_id"] = players["player_id"].astype(int)

    performances = pick(perf, PERF_MAP).dropna(subset=["player_id"])
    performances["player_id"] = performances["player_id"].astype(int)
    for col in ("matches", "goals", "assists", "minutes"):
        performances[col] = pd.to_numeric(performances[col], errors="coerce").fillna(0).astype(int)
    performances = performances[performances["player_id"].isin(players["player_id"])]

    database.init_db()
    conn = database.get_db()
    players.to_sql("players", conn, if_exists="append", index=False)
    performances.to_sql("performances", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()
    print(f"Loaded {len(players)} players and {len(performances)} performance rows.")


if __name__ == "__main__":
    main()
