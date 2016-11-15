from time import sleep
import sys
import json
import time

#custom class
from airbox.querySiteID import querySiteID
from airbox.parseSite import parseSite


def main():
	cityList = ['taipei', 'newtaipei', 'taichung', 'tainan', 'kaohsiung']
	option = sys.argv[1]

	if option == '-q':
		print('>>> Query site ID: All')
		query = querySiteID(cityList)

	elif option == '-p':
		arg_city = sys.argv[2]
		database = 'AirBox_new'

		with open('siteID.json') as file:
			data = json.load(file)

		#parse site data
		while True:
			parse = parseSite(arg_city, data[arg_city], database)
			parse.parseData()
			sleep(180)


if __name__ == '__main__':
	main()
