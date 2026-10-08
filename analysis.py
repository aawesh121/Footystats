"""Pure analysis functions (no Flask, no DB) so they are easy to test."""


def per90(value, minutes):
    """Rate per 90 minutes, rounded to 2 decimals. 0 if no minutes."""
    if not minutes:
        return 0.0
    return round(value * 90 / minutes, 2)


def season_totals(rows):
    """Group performance rows by season -> list of dicts sorted by season."""
    seasons = {}
    for r in rows:
        s = seasons.setdefault(
            r["season"], {"season": r["season"], "matches": 0, "goals": 0, "assists": 0, "minutes": 0}
        )
        for k in ("matches", "goals", "assists", "minutes"):
            s[k] += r[k] or 0
    out = []
    for s in sorted(seasons.values(), key=lambda x: x["season"] or ""):
        s["contributions"] = s["goals"] + s["assists"]
        s["goals_per90"] = per90(s["goals"], s["minutes"])
        s["assists_per90"] = per90(s["assists"], s["minutes"])
        out.append(s)
    return out


def summarize(rows):
    """Career totals, per-90 rates and best season (by goal contributions)."""
    seasons = season_totals(rows)
    goals = sum(s["goals"] for s in seasons)
    assists = sum(s["assists"] for s in seasons)
    minutes = sum(s["minutes"] for s in seasons)
    best = max(seasons, key=lambda s: s["contributions"], default=None)
    return {
        "goals": goals,
        "assists": assists,
        "contributions": goals + assists,
        "minutes": minutes,
        "goals_per90": per90(goals, minutes),
        "assists_per90": per90(assists, minutes),
        "best_season": best["season"] if best else None,
        "best_season_contributions": best["contributions"] if best else 0,
        "seasons": seasons,
    }
