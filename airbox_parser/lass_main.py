from time import time, sleep
import sys
import json

#custom class
from airbox.parseSite import parseSite


def main():
	arg_src = sys.argv[1]
	database = 'AirBox_test'

	#parse site data
	parse = parseSite(arg_src, database)
	while True:
		start = time()	#debug
		parse.parseData()
		print('Execution: ' + str(time() - start) + ' sec')	#debug
		sleep(300)	#debug


if __name__ == '__main__':
	main()
