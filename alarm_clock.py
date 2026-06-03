# alarm_clock.py — entry point + CLI
import argparse
import sys
from datetime import datetime

from alarm_store import add_alarm, get_all_alarms, remove_alarm


def parse_time(time_str: str) -> str:
    """Validate and normalise time input to HH:MM (24-hour)."""
    for fmt in ("%H:%M", "%I:%M%p", "%I:%M %p"):
        try:
            return datetime.strptime(time_str.strip(), fmt).strftime("%H:%M")
        except ValueError:
            continue
    print(f"Error: '{time_str}' is not a valid time. Use HH:MM (e.g. 07:30).")
    sys.exit(1)


def cmd_set(args: argparse.Namespace) -> None:
    time_str = parse_time(args.time)

    now = datetime.now().strftime("%H:%M")
    if time_str <= now:
        print(f"Error: {time_str} is in the past. Set a future time.")
        sys.exit(1)

    label = (args.label or "")[:40]  # cap label at 40 chars to keep list readable

    existing = [a for a in get_all_alarms() if a["time"] == time_str]
    if existing:
        print(f"Warning: an alarm already exists at {time_str} (id={existing[0]['id']}). Adding anyway.")

    alarm = add_alarm(time_str, label)
    print(f"Alarm set  id={alarm['id']}  time={alarm['time']}" + (f"  label={alarm['label']!r}" if label else ""))


def cmd_list(args: argparse.Namespace) -> None:
    alarms = get_all_alarms()
    if not alarms:
        print("No alarms set.")
        return
    print(f"{'ID':<10} {'TIME':<8} LABEL")
    print("-" * 35)
    for a in alarms:
        print(f"{a['id']:<10} {a['time']:<8} {a['label']}")


def cmd_cancel(args: argparse.Namespace) -> None:
    if remove_alarm(args.id):
        print(f"Alarm {args.id} cancelled.")
    else:
        print(f"No alarm found with id={args.id}")
        sys.exit(1)


def cmd_start(args: argparse.Namespace) -> None:
    from alarm_runner import run_daemon
    print("Alarm daemon started. Press Ctrl+C or run 'alarm_clock.py exit' to stop.")
    try:
        run_daemon()
    except KeyboardInterrupt:
        print("\nAlarm clock stopped. Goodbye.")


def cmd_exit(args: argparse.Namespace) -> None:
    print("To stop the daemon, press Ctrl+C in the terminal where it is running.")
    print("All pending alarms are saved and will fire when you restart.")
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="alarm_clock",
        description="A simple command-line alarm clock.",
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    p_set = sub.add_parser("set", help="Set a new alarm  e.g. set 07:30 'Wake up'")
    p_set.add_argument("time", help="Alarm time in HH:MM format (24-hour)")
    p_set.add_argument("label", nargs="?", default="", help="Optional label")
    p_set.set_defaults(func=cmd_set)

    p_list = sub.add_parser("list", help="List all pending alarms")
    p_list.set_defaults(func=cmd_list)

    p_cancel = sub.add_parser("cancel", help="Cancel an alarm by ID")
    p_cancel.add_argument("id", help="Alarm ID (from 'list')")
    p_cancel.set_defaults(func=cmd_cancel)

    p_start = sub.add_parser("start", help="Start the alarm daemon (blocking)")
    p_start.set_defaults(func=cmd_start)

    p_exit = sub.add_parser("exit", help="Show how to stop the daemon gracefully")
    p_exit.set_defaults(func=cmd_exit)

    return parser


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
