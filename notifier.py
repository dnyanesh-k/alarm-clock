import os
import sys
import time
from datetime import datetime, timedelta

from alarm_store import log_fired, log_snoozed, add_alarm, remove_alarm


_BOLD  = "\033[1m"
_RED   = "\033[31m"
_RESET = "\033[0m"


def _beep() -> None:
    if os.name == "nt":
        import winsound
        for _ in range(4):
            winsound.Beep(1000, 500)
            time.sleep(0.2)
    elif _is_wsl():
        for _ in range(4):
            os.system("powershell.exe -c '[console]::beep(1000,400)' 2>/dev/null")
            time.sleep(0.3)
    else:
        for _ in range(4):
            sys.stdout.write("\a")
            sys.stdout.flush()
            time.sleep(0.3)


def _is_wsl() -> bool:
    try:
        return "microsoft" in open("/proc/version").read().lower()
    except OSError:
        return False


def fire(alarm: dict) -> None:
    log_fired(alarm)
    remove_alarm(alarm["id"])

    label = f"  {alarm['label']}" if alarm["label"] else ""
    _beep()
    print(f"\n{_BOLD}{_RED}{'=' * 40}{_RESET}")
    print(f"{_BOLD}{_RED}  ALARM  {alarm['time']}{label}{_RESET}")
    print(f"{_BOLD}{_RED}{'=' * 40}{_RESET}")
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
