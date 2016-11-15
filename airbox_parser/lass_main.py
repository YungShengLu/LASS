from time import time, sleep
import sys
import json

#custom class
from airbox.querySiteID import querySiteID
from airbox.parseSite import parseSite


def main():
	cityList = ['taipei', 'newtaipei', 'taichung', 'tainan', 'kaohsiung']
	option = sys.argv[1]

	if option == '-q':
		print('>>> Query site ID: All')
		query = querySiteID(cityList)

		with open('siteID.json', 'w', encoding = 'utf-8-sig') as file:
			json.dump(query.queryID(), file)

	elif option == '-p':
		arg_city = sys.argv[2]
		database = 'AirBox_test'

		with open('siteID.json', encoding = 'utf-8-sig') as file:
			data = json.load(file)

		#parse site data
		parse = parseSite(arg_city, data[arg_city], database)
		while True:
			start = time()	#debug
			parse.parseData()
			print('Execution: ' + time() - start + ' sec')	#debug
			#sleep(20)	#debug


if __name__ == '__main__':
	main()
