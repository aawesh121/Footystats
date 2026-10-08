# Soccer Player Analyzer

A small Flask + SQLite web app to search football players, view their profile and season
statistics, and see goals/assists per 90 with a simple chart. Built by two friends with an
equal 50/50 split of work (see [ROADMAP.md](ROADMAP.md)).

## MVP
- Player search
- Profile with image and basic info
- Season / team / competition statistics
- Total goals, assists, goal contributions
- Goals per 90 and assists per 90, best season
- Latest market value
- One season-performance chart (Chart.js)

## Stack
Python · Flask · SQLite · Pandas · HTML/CSS/Bootstrap/Jinja · Chart.js · Git/GitHub

## Setup
```bash
git clone <your-repo-url>
cd soccer-player-analyzer
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Load the data
1. Put `player_profiles.csv` and `player_performances.csv` in `data/`.
2. (Optional) see the columns: `python scripts/load_data.py --inspect`
3. Build the database: `python scripts/load_data.py`

If your CSV column names differ, edit `PROFILE_MAP` / `PERF_MAP` in `scripts/load_data.py`.

## Run
```bash
python app.py
```
Open http://127.0.0.1:5000

## Test
```bash
pytest
```

## Structure
```
soccer-player-analyzer/
├── app.py            # Flask routes
├── database.py       # SQLite schema + queries
├── analysis.py       # totals, per-90, best season
├── data/             # CSVs + players.db (git-ignored)
├── scripts/load_data.py
├── templates/        # base, home, search, player
├── static/           # css, images
└── tests/
```

## Team workflow
Learn → Build → Test → Explain → Review → Commit → Merge

- Never commit to `main` directly; use feature branches (`feature/search-backend`, `feature/search-ui`).
- Open a Pull Request; the *other* friend reviews and explains it before merging.
- Switch roles every week so both learn frontend, backend, data and testing.
- Commit style: `feat: add search route`, `fix: per-90 divide by zero`, `docs: update README`.

## Out of scope
No ML/AI predictions, login, admin panel, live scores, tactics, or huge dashboards.
