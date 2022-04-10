#!/usr/bin/env python3
import subprocess

import sys
import os


def main():
    global decoder, alert_raiser, alert_display, boat_counter
    decoder = subprocess.Popen(
        'xterm -e python3 ./ais-decoder.py &', shell=True)
    alert_raiser = subprocess.Popen(
        'xterm -e python3 ./speed_alert_raiser.py &', shell=True)
    alert_display = subprocess.Popen(
        'xterm -e python3 ./alert_display.py &', shell=True)
    boat_counter = subprocess.Popen(
        'xterm -e python3 ./boat_type_counter.py &', shell=True)
    i = ""
    while(1):
        i = input(
            "Enter S to simulate a new boat, R to reset the counter or Ctrl+C to quit\n").capitalize()
        if (i == 'S'):
            exec(open("ais-simulator.py").read())
        elif (i == 'R'):
            exec(open("manual_reset.py").read())


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        for process in [decoder, alert_raiser, alert_display, boat_counter]:
            process.kill()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
