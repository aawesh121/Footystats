import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import app as app_module
import database


def make_db(tmp_path, monkeypatch):
    path = tmp_path / "t.db"
    database.init_db(path)
    conn = database.get_db(path)
    conn.execute("INSERT INTO players (player_id, name, position) VALUES (1, 'Test Player', 'Forward')")
    conn.execute("INSERT INTO performances (player_id, season, team, competition, matches, goals, assists, minutes) "
                 "VALUES (1, '20/21', 'FC Test', 'League', 30, 10, 5, 2700)")
    conn.commit()
    conn.close()
    monkeypatch.setattr(database, "DB_PATH", path)
    for fn in ("search_players", "get_player", "get_performances"):
        orig = getattr(database, fn)
        monkeypatch.setattr(database, fn, lambda *a, _o=orig, **k: _o(*a, path=path, **k))


def test_search_and_profile(tmp_path, monkeypatch):
    make_db(tmp_path, monkeypatch)
    c = app_module.app.test_client()
    assert b"Test Player" in c.get("/search?q=test").data
    r = c.get("/player/1")
    assert r.status_code == 200 and b"Test Player" in r.data
    assert c.get("/player/999").status_code == 404
