# pomodoro
A simple timer that can be used for pomodoros on mac.

usage
- pomodoro 25 (working)
- pomodoro -b 5 (break)

further options
- -r activate for sound notification (ring)
- -s show the log of the day

more functionality:
- logging the amount of time spent working/break to ~/.pomodoro/2026-06-12 
  - entries should be simple, for example "WORK 25min \nPAUSE 5min \nWORK 20min (Stopped after 16min)"
- have the screen updated every 0.2 seconds
- do not count remaining down, but use timestamp, calculate elapsed time and show that on the screen (more robust and precise)