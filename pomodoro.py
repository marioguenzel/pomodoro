#!/usr/bin/env python3
import sys, time, subprocess, argparse
from datetime import date, datetime
from pathlib import Path

LOG_DIR = Path.home() / ".pomodoro"
BAR_WIDTH = 20


def log_entry(line):
    LOG_DIR.mkdir(exist_ok=True)
    with open(LOG_DIR / date.today().isoformat(), "a") as f:
        f.write(line + "\n")


def show_log():
    logfile = LOG_DIR / date.today().isoformat()
    if logfile.exists():
        print(logfile.read_text(), end="")
    else:
        print("No log for today.")


def notify(label, ring):
    if ring:
        subprocess.Popen(["afplay", "/System/Library/Sounds/Glass.aiff"])
    msg = "Pomodoro done! Time for a break." if label == "WORK" else "Break is over! Back to work."
    subprocess.run(["osascript", "-e", f'''
    display dialog "{msg}" ¬
        with title "Pomodoro" ¬
        buttons {{"Dismiss"}} ¬
        default button "Dismiss"
    '''], stdout=subprocess.DEVNULL)


def run_timer(minutes, label, ring, note):
    total = minutes * 60
    start = time.monotonic()
    started_at = datetime.now().strftime("%H:%M")
    suffix = f" - {note}" if note else ""

    try:
        while True:
            elapsed = min(time.monotonic() - start, total)
            m, s = divmod(int(elapsed), 60)
            filled = int(BAR_WIDTH * elapsed / total) if total else BAR_WIDTH
            bar = "█" * filled + "░" * (BAR_WIDTH - filled)
            print(f"\r  {label}  {bar}  {m:02d}:{s:02d} / {minutes:02d}:00 {suffix}",
                  end="", flush=True)
            if elapsed >= total:
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        elapsed = time.monotonic() - start
        m, s = divmod(int(elapsed), 60)
        log_entry(f"{started_at} {label} {int(elapsed // 60)}/{minutes}min{suffix}")
        print(f"\n  Stopped after {m:02d}:{s:02d}.")
        sys.exit(0)

    print(f"\n  Done!")
    log_entry(f"{started_at} {label} {minutes}min{suffix}")
    notify(label, ring)


def main():
    parser = argparse.ArgumentParser(description="A simple pomodoro timer.")
    parser.add_argument("minutes", nargs="?", type=int, default=None,
                        help="work/break duration in minutes (default: 25/5)")
    parser.add_argument("-b", "--break", action="store_true", dest="brk",
                        help="take a break instead")
    parser.add_argument("-r", "--ring", action="store_true",
                        help="play a sound when the timer finishes")
    parser.add_argument("-s", "--show", action="store_true",
                        help="show the log of the day")
    parser.add_argument("-n", "--note", metavar="TEXT",
                        help="note to append to the log entry")
    args = parser.parse_args()

    if args.show:
        show_log()
        return


    if args.brk:
        minutes = 5
        if args.minutes is not None:
            minutes = args.minutes
        run_timer(minutes, "BREAK", args.ring, args.note)
    else:
        minutes = 25
        if args.minutes is not None:
            minutes = args.minutes
        run_timer(minutes, "WORK", args.ring, args.note)


if __name__ == "__main__":
    main()
