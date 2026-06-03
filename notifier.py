# notifier.py — cross-platform sound + terminal output
import os
import sys
from datetime import datetime, timedelta

from alarm_store import log_fired, log_snoozed, add_alarm, remove_alarm


def _beep() -> None:
    if os.name == "nt":
        import winsound
        winsound.Beep(1000, 800)
    else:
        sys.stdout.write("\a")
        sys.stdout.flush()


def fire(alarm: dict) -> None:
    log_fired(alarm)
    remove_alarm(alarm["id"])

    label = f"  [{alarm['label']}]" if alarm["label"] else ""
    print(f"\n{'=' * 40}")
    print(f"  ALARM  {alarm['time']}{label}")
    print(f"{'=' * 40}")
    _beep()
    print("  [s] Snooze 5 min    [d] Dismiss")

    choice = _prompt_choice()
    if choice == "s":
        snooze(alarm)
    else:
        print(f"  Alarm {alarm['id']} dismissed.")


def snooze(alarm: dict) -> None:
    snooze_time = (
        datetime.now() + timedelta(minutes=5)
    ).strftime("%H:%M")

    new_alarm = add_alarm(snooze_time, alarm["label"])
    log_snoozed(alarm, snooze_time)
    print(f"  Snoozed — new alarm at {snooze_time}  id={new_alarm['id']}")


def _prompt_choice() -> str:
    while True:
        try:
            choice = input("  > ").strip().lower()
            if choice in ("s", "d"):
                return choice
            print("  Enter 's' to snooze or 'd' to dismiss.")
        except (EOFError, KeyboardInterrupt):
            return "d"
