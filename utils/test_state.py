import json
from pathlib import Path
from datetime import datetime

# Dinamik konfiguratsiya
CONFIG = {
    "max_failures_before_skip": 3,  # ❗️ nechta fail bo‘lsa, keyingi testlar skip qilinadi
    "retry_count": 1                # ❗️ fail bo‘lsa, test nechta marta qayta chaqiriladi
}

STATE_FILE = Path(__file__).parent.parent / "test_state.json"

_current_session_key = None

def start_new_session():
    """Har pytest sessiyasi uchun yangi blok ochadi"""
    global _current_session_key
    _current_session_key = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    data = {}
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}

    # Yangi sessiya ochamiz: tests bo‘sh, stats nol
    data[_current_session_key] = {
        "tests": {},
        "stats": {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
    }

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_states():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_state(test_name: str, status: str, attempt: int = None, error: str = None):
    """Hozirgi sessiya bo‘yicha test holatini yozish (retry tarixi bilan)"""
    data = load_states()

    global _current_session_key
    if not _current_session_key:
        start_new_session()

    if _current_session_key not in data:
        data[_current_session_key] = {"tests": {}, "stats": {"total": 0, "passed": 0, "failed": 0, "skipped": 0}}

    session = data[_current_session_key]

    # Agar test allaqachon mavjud bo‘lsa → yangilash
    if test_name not in session["tests"]:
        session["tests"][test_name] = {"status": None, "attempts": []}

    test_entry = session["tests"][test_name]

    # Retry urinishini log qilamiz
    if attempt is not None:
        test_entry["attempts"].append({"attempt": attempt, "status": status, "error": error})

    # Oxirgi statusni yangilaymiz
    test_entry["status"] = status

    # Statistikani yangilaymiz
    stats = session["stats"]
    stats["total"] = len(session["tests"])
    stats["passed"] = sum(1 for t in session["tests"].values() if t["status"] == "passed")
    stats["failed"] = sum(1 for t in session["tests"].values() if t["status"] == "failed")
    stats["skipped"] = sum(1 for t in session["tests"].values() if t["status"] == "skipped")

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def can_continue():
    """
    Oxirgi sessiyada nechta fail bo‘lganini tekshiradi.
    Fail soni limitdan oshsa -> False qaytaradi (ya'ni keyingi testlar skip bo‘ladi).
    """
    data = load_states()
    if not data:
        return True

    last_session = sorted(data.keys())[-1]
    stats = data[last_session].get("stats", {})
    max_failures = CONFIG["max_failures_before_skip"]

    return stats.get("failed", 0) < max_failures
