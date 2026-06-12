#!/usr/bin/env python3
import sys, time, subprocess, argparse
from datetime import date
from pathlib import Path

LOG_DIR = Path.home() / ".pomodoro"


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


def run_timer(minutes, label, ring):
    total = minutes * 60
    start = time.monotonic()

    print(f"\t\t-----")
    print(f"\t\t{label}")
    print(f"\t\t-----", end="", flush=True)
    print("\033[1A", end="")  # move cursor up onto the middle line

    try:
        while True:
            elapsed = time.monotonic() - start
            if elapsed >= total:
                elapsed = total
            m, s = divmod(int(elapsed), 60)
            print(f"\r\t\t{m:02d}:{s:02d} / {minutes:02d}:00\t\t", end="", flush=True)
            if elapsed >= total:
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        stopped_after = int((time.monotonic() - start) // 60)
        log_entry(f"{label} {minutes}min (Stopped after {stopped_after}min)")
        print("\nStopped.")
        sys.exit(0)

    print()
    log_entry(f"{label} {minutes}min")
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
    args = parser.parse_args()

    if args.show:
        show_log()
        return


    if args.brk:
        minutes = 5
        if args.minutes is not None:
            minutes = args.minutes
        run_timer(minutes, "PAUSE", args.ring)
    else:
        minutes = 25
        if args.minutes is not None:
            minutes = args.minutes
        run_timer(minutes, "WORK", args.ring)


if __name__ == "__main__":
    main()
