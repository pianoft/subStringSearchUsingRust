import subprocess
import sys


def say(files):
    subprocess.run(['spd-say -w -r 50 -i 100 "'+files+'";'], shell=True)
    return

say(sys.argv[1])
