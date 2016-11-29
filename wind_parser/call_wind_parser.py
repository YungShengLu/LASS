from subprocess import call
import time
from datetime import datetime
while True:
	print ('Current Wind Parser execution timestamp:', time.gmtime())
	call(["python3","wind_parser.py"])
	time.sleep(3600)
