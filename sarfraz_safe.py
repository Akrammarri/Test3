# sarfraz_safe.py
# Safe, open-source replacement for development/testing only.
# MIT License (c) You

import re
import uuid
import time
from threading import Thread, Lock

_sessions = {}
_sessions_lock = Lock()

def parse_cards_from_text(input_text):
    cards = []
    for line in input_text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) >= 4:
            cardnum = parts[0].strip()
            cards.append({"card": "|".join(parts[:4]), "number": cardnum})
    return {"success": True, "cards": cards}

def _simulate_check_card(card_entry):
    num = card_entry.get("number", "")
    last = num[-1] if num else "0"
    try:
        lastd = int(last)
    except:
        lastd = 0
    status = "live" if lastd % 2 == 0 else "dead"
    return {
        "card": card_entry.get("card"),
        "status": status,
        "message": "Simulated safe response",
        "check_time": 0.05,
        "bin_info": {
            "brand": "MockBrand",
            "type": "credit",
            "scheme": "visa" if str(num).startswith("4") else "unknown",
            "bank": {"name": "Mock Bank"},
            "country": {"name": "Neverland", "emoji": "🏳️"}
        }
    }

def start_checking(cards, gateway="safe"):
    if not isinstance(cards, list):
        return {"success": False, "error": "cards must be a list"}

    session_id = str(uuid.uuid4())
    with _sessions_lock:
        _sessions[session_id] = {
            "status": "processing",
            "results": [],
            "counters": {"total": len(cards), "total_checked": 0}
        }

    def worker(sid, card_list):
        for c in card_list:
            time.sleep(0.15)
            r = _simulate_check_card(c)
            with _sessions_lock:
                _sessions[sid]["results"].append(r)
                _sessions[sid]["counters"]["total_checked"] += 1
        with _sessions_lock:
            _sessions[sid]["status"] = "completed"

    Thread(target=worker, args=(session_id, cards), daemon=True).start()
    return {"success": True, "session_id": session_id}

def get_progress(session_id):
    with _sessions_lock:
        s = _sessions.get(session_id)
        if not s:
            return {"success": False, "error": "unknown session"}
        return {
            "success": True,
            "status": s["status"],
            "results": list(s["results"]),
            "counters": dict(s["counters"])
        }

def _reset_all_sessions():
    with _sessions_lock:
        _sessions.clear()
