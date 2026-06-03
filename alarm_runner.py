# alarm_runner.py — threading, fire/snooze/cancel logic
import time
from datetime import datetime

from alarm_store import get_all_alarms
from notifier import fire

POLL_INTERVAL = 30  # seconds


def _due_alarms() -> list[dict]:
    now = datetime.now().strftime("%H:%M")
    return [a for a in get_all_alarms() if a["time"] == now]


def run_daemon() -> None:
    print(f"Checking alarms every {POLL_INTERVAL}s. Current time: {datetime.now().strftime('%H:%M')}")
    while True:
        for alarm in _due_alarms():
            fire(alarm)
        time.sleep(POLL_INTERVAL)
