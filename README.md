# alarm-clock-cli

A lightweight command-line alarm clock written in pure Python (stdlib only, no dependencies).

## Requirements

- Python 3.8+
- No `pip install` needed
- WSL / Linux / macOS / Windows supported

## Usage

### Start the alarm daemon (keep this terminal open)
```bash
python3 alarm_clock.py start
```

### Set an alarm
```bash
python3 alarm_clock.py set 07:30
python3 alarm_clock.py set 14:05 "Team standup"
```

### List all pending alarms
```bash
python3 alarm_clock.py list
```

### Cancel an alarm by ID
```bash
python3 alarm_clock.py cancel <id>
```

### Stop the daemon
Press `Ctrl+C` in the terminal where `start` is running, or from another terminal:
```bash
python3 alarm_clock.py exit
```

### When an alarm fires
You will see a bold red alert and hear 4 beeps. Press:
- `s` — snooze for 5 minutes
- `d` — dismiss

## Platform notes

| Platform | Sound |
|---|---|
| WSL (Ubuntu on Windows) | Uses `powershell.exe` beep — works out of the box |
| Linux (native) | Terminal bell (`\a`) — enable bell in your terminal settings |
| Windows | `winsound.Beep` — built-in |

## Data files

Alarms and logs are stored outside the repo so they are never committed:

| File | Location |
|---|---|
| Alarms | `~/alarm_clock/alarms.json` (Linux/WSL) or `%APPDATA%\alarm_clock\alarms.json` (Windows) |
| Log | `~/alarm_clock/alarm_clock.log` |

## Engineering decisions

| Decision | Choice | Reason |
|---|---|---|
| Persistence | JSON file in home dir | Zero deps, survives restarts, never committed |
| Notification | `powershell.exe` (WSL) / `winsound` (Win) / `\a` (Linux) | Stdlib + OS-native, no audio libraries |
| Daemon loop | `time.sleep` polling every 30s | Simple, predictable, no scheduler deps |
| CLI | `argparse` | Stdlib, no install required |
| Snooze | 5-minute fixed | Core UX at minimal complexity |
| Duplicate alarms | Warn, don't block | Two meetings at same time is valid |

## Project structure

```
alarm_clock.py    # entry point + argparse CLI
alarm_store.py    # load/save alarms to JSON + logging
alarm_runner.py   # daemon loop, fires due alarms
notifier.py       # cross-platform sound + ANSI visual alert
```
