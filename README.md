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

## AI-assisted development process

This project was built using AI as a coding assistant. The process was intentionally directed rather than just generated:

**Problem definition first**
Before writing code, I used AI to reason through scope — what "alarm clock" means as a CLI tool, what to cut (recurring alarms, TUI, database), and what the minimum viable feature set was. The goal was to define the problem clearly before touching implementation.

**Directed reviews, not blind generation**
At each step I directed specific review questions rather than accepting output blindly:

- *"Does the JSON schema support adding recurrence later without a breaking change?"* — confirmed the flat structure is extensible
- *"Does the polling approach have any race conditions if two alarms fire at the same second?"* — reviewed and confirmed safe: `_due_alarms()` returns a list, each alarm is processed sequentially in the same thread, no concurrent writes
- *"Is a background thread needed or is a simple loop sufficient?"* — `threading.Timer` was initially considered but rejected; a `while True` + `time.sleep(30)` loop is simpler, easier to reason about, and sufficient for a single-user CLI tool where alarms fire at most once per minute
- *"Why are notifier and runner being committed together?"* — caught that they should be tested and committed independently; each module is independently testable

**Validated incrementally**
Each module was tested in isolation before the next was built:
1. `alarm_store` tested via Python REPL — verified JSON read/write and log output
2. `notifier` tested standalone with a fake alarm dict — verified sound and prompt
3. `alarm_runner` tested by injecting a due alarm — verified daemon loop fires correctly
4. Full end-to-end test with a real alarm set 2 minutes ahead

**Known limitation documented, not hidden**
The past-time check uses string comparison (`HH:MM`), which works correctly within a single day but will not reject `23:59` set just after midnight. This is a known trade-off — adding `datetime` arithmetic for a single edge case was not worth the complexity for a local CLI tool.

## Project structure

```
alarm_clock.py    # entry point + argparse CLI
alarm_store.py    # load/save alarms to JSON + logging
alarm_runner.py   # daemon loop, fires due alarms
notifier.py       # cross-platform sound + ANSI visual alert
```
