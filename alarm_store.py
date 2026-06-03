# alarm_store.py — persistence layer
import json
import logging
import os
import uuid
from pathlib import Path


def _data_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path.home()
    data_dir = base / "alarm_clock"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


STORE_PATH = _data_dir() / "alarms.json"
LOG_PATH = _data_dir() / "alarm_clock.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def _load() -> list[dict]:
    if not STORE_PATH.exists():
        return []
    try:
        return json.loads(STORE_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return []


def _save(alarms: list[dict]) -> None:
    STORE_PATH.write_text(json.dumps(alarms, indent=2))


def add_alarm(time_str: str, label: str = "") -> dict:
    alarm = {
        "id": str(uuid.uuid4())[:8],
        "time": time_str,
        "label": label,
    }
    alarms = _load()
    alarms.append(alarm)
    _save(alarms)
    logger.info("SET   id=%s time=%s label=%r", alarm["id"], time_str, label)
    return alarm


def remove_alarm(alarm_id: str) -> bool:
    alarms = _load()
    remaining = [a for a in alarms if a["id"] != alarm_id]
    if len(remaining) == len(alarms):
        return False
    _save(remaining)
    logger.info("CANCEL id=%s", alarm_id)
    return True


def get_all_alarms() -> list[dict]:
    return _load()


def log_fired(alarm: dict) -> None:
    logger.info("FIRED  id=%s time=%s label=%r", alarm["id"], alarm["time"], alarm["label"])


def log_snoozed(alarm: dict, snoozed_to: str) -> None:
    logger.info("SNOOZE id=%s snoozed_to=%s", alarm["id"], snoozed_to)
