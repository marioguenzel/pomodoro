# 🍅 Pomodoro Timer for Mac

A dead-simple pomodoro timer for the macOS terminal. One Python file, no dependencies, with a live progress bar and a plain-text daily log.

```
  WORK  ████████░░░░░░░░░░░░  10:23 / 25:00  - writing paper
```


## Usage

```bash
pomodoro              # 25 min work session
pomodoro 40           # 40 min work session
pomodoro -b           # 5 min break
pomodoro -b 15        # 15 min break
pomodoro -r           # ring a sound when the timer finishes
pomodoro -n "emails"  # attach a note to the session
pomodoro -s           # show today's log
```

Options can be combined, e.g. `pomodoro 50 -r -n "deep work"`.

Stop a running timer at any time with `Ctrl+C` — the partial session is still logged.

| Option | Description |
|---|---|
| `minutes` | Duration in minutes (default: 25 for work, 5 for break) |
| `-b`, `--break` | Run a break instead of a work session |
| `-r`, `--ring` | Play a sound when the timer finishes |
| `-n`, `--note TEXT` | Note shown on screen and appended to the log entry |
| `-s`, `--show` | Print today's log and exit |


## Logging

Every session is appended to a plain-text file per day at `~/.pomodoro/YYYY-MM-DD`:

```
09:15 WORK 25min - writing paper
09:42 BREAK 5min
09:48 WORK 16/25min - emails
```

Each entry records the start time, the session type, the duration, and the optional note. Sessions stopped early with `Ctrl+C` are logged as `elapsed/planned` (e.g. `16/25min`), so completed and interrupted sessions are easy to tell apart.

Since the logs are just text files, they play nicely with standard tools:

```bash
cat ~/.pomodoro/2026-06-12            # any past day
grep -c WORK ~/.pomodoro/2026-06-12   # number of work sessions that day
grep "writing paper" ~/.pomodoro/*    # find all sessions for a project
```


## How it works

- The timer is **timestamp-based**: it records the start time once and computes the elapsed time on every refresh, instead of counting down with `sleep(1)`. This keeps it accurate even over long sessions — sleep-based countdowns drift.
- The display refreshes every 0.2 s on a single line, so `Ctrl+C` responds almost instantly.
- When a timer finishes, a native macOS dialog pops up (via `osascript`); with `-r` it also plays the system "Glass" sound (via `afplay`).


## Installation

Requires macOS and Python 3 (preinstalled on recent macOS). No packages to install.

**Option 1 — shell alias (recommended):** keep the script wherever you like and add an alias to your `~/.zshrc`:

```bash
alias pomodoro="clear && python3 /path/to/pomodoro.py"
```

The `clear` gives every session a clean, distraction-free screen. Reload with `source ~/.zshrc` (or open a new terminal), then run `pomodoro` from anywhere.

**Option 2 — put it on your PATH:**

```bash
chmod +x pomodoro.py
mv pomodoro.py /usr/local/bin/pomodoro   # or any directory on your PATH
```


## License

"THE BEER-WARE LICENSE" (Revision 42): 
marioguenzel wrote this. As long as you retain this notice you can do whatever you want with this stuff. If this stuff is worth it, you can buy me a beer in return. Mario Guenzel 🍺
