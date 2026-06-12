#!/usr/bin/env python3
import sys, time, subprocess

minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 25
remaining = minutes * 60

print("\t\t-----")
print("\t\tTIME")
print("\t\t-----", end="", flush=True)
print("\033[1A", end="")

try:
    while remaining >= 0:
        m, s = divmod(remaining, 60)

        print(f"\r\t\t{m:02d}:{s:02d}\t\t", end="", flush=True)
        if remaining == 0:
            break
        time.sleep(1)
        remaining -= 1
except KeyboardInterrupt:
    print("\nStopped.")
    sys.exit(0)

print()
subprocess.Popen(["afplay", "/System/Library/Sounds/Glass.aiff"])  # play a sound (non-blocking, so it overlaps with the dialog)
subprocess.run(["osascript", "-e", '''
display dialog "Pomodoro done! Time for a break." ¬
    with title "Pomodoro" ¬
    buttons {"Dismiss"} ¬
    default button "Dismiss"
'''])
