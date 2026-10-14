"""Sauvegarde des scores dans un fichier JSON local (côté serveur)."""
import json
from datetime import datetime
from pathlib import Path

SCORES_FILE = Path(__file__).parent / "scores.json"


def _load():
    if not SCORES_FILE.exists():
        return []
    try:
        return json.loads(SCORES_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _save(games):
    SCORES_FILE.write_text(
        json.dumps(games, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def top_scores(limit=10):
    """Meilleur score de chaque joueur, trié du plus grand au plus petit."""
    best = {}
    for game in _load():
        key = game["name"].lower()
        if key not in best or game["score"] > best[key]["score"]:
            best[key] = game
    return sorted(best.values(), key=lambda g: g["score"], reverse=True)[:limit]


def add_score(name, score):
    """Enregistre une partie. Renvoie le rang et si c'est un record."""
    games = _load()
    all_scores = [g["score"] for g in games]
    mine = [g["score"] for g in games if g["name"].lower() == name.lower()]
    games.append(
        {"name": name, "score": score, "date": datetime.now().isoformat(timespec="seconds")}
    )
    _save(games)

    board = top_scores(10)
    rank = next(
        (i for i, g in enumerate(board, 1) if g["name"].lower() == name.lower()), None
    )
    return {
        "rank": rank,
        "absolute_record": score > max(all_scores, default=-1),
        "personal_best": score > max(mine, default=-1),
    }
