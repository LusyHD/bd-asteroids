import json
from pathlib import Path

_score = 0
_high_score = 0
_prev_high_score = None
_path = Path("highscore.json")

def load():
    global _high_score
    if _path.exists():
        try:
            _high_score = json.loads(_path.read_text()).get("high_score", 0)
        except Exception:
            _high_score = 0

def save():
    try:
        _path.write_text(json.dumps({"high_score": _high_score}))
    except Exception:
        pass  # ignore write failures for now

def reset():
    global _score
    _score = 0
    _prev_high_score = None

def add(points=1):
    global _score, _high_score, _prev_high_score
    _score += points
    if _score > _high_score:
        if _prev_high_score is None:
            _prev_high_score = _high_score
        _high_score = _score
        save()

def get(): 
    return _score

def get_high(): 
    return _high_score

def get_prev_high():
    return _prev_high_score
