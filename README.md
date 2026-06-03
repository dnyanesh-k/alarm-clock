# alarm-clock-cli

A lightweight command-line alarm clock written in pure Python (stdlib only, no dependencies).

## Requirements

- Python 3.8+
- No `pip install` needed

## Usage

### Start the alarm daemon (blocking — keep this terminal open)
```bash
python alarm_clock.py start
```

### Set an alarm
```bash
python alarm_clock.py set 07:30
python alarm_clock.py set 14:05 "Team standup"
```

### List all pending alarms
```bash
python alarm_clock.py list
```

### Cancel an alarm by ID
```bash
python alarm_clock.py cancel <id>
```

### Snooze a firing alarm
When an alarm fires you will be prompted — press `s` to snooze 5 minutes or `d` to dismiss.

## How it works

- Alarms are stored in `~/.alarm_clock.json` (survives restarts).
- The `start` command runs a background loop that checks every 30 seconds and fires alarms at the right time.
- Notification is a terminal bell (`\a`) + a printed message — no external audio libraries needed.

## Engineering decisions

| Decision | Choice | Reason |
|---|---|---|
| Persistence | JSON file (`~/.alarm_clock.json`) | Zero deps, survives restarts |
| Notification | `winsound` (Windows) / `\a` bell (Unix) | Stdlib only, cross-platform |
| Concurrency | `threading.Timer` | Non-blocking, simple for this scale |
| CLI | `argparse` | Stdlib, no install required |
| Snooze | 5-minute fixed snooze | Core UX, minimal complexity |

## Project structure

```
alarm_clock.py    # entry point + argparse CLI
alarm_store.py    # load/save alarms to JSON
alarm_runner.py   # threading + fire/snooze/cancel logic
notifier.py       # cross-platform sound + terminal output
```
