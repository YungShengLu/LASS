from subprocess import call
import time
while True:
      call(["python3","wind_parser.py"])
      time.sleep(3600)
