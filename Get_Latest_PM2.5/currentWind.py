# fetch wind data each hour
import sys
import re
import os
import json
import time

from influxdb import InfluxDBClient
import uniout

connectDB='LASS_WIND'
client = InfluxDBClient('localhost', 8086, 'root', 'root', connectDB) 
client.create_database(connectDB) 



def main():

	# read wind location csv to link id to name
	windIDs = {}
	f = open("wind_location.csv", 'r')
	lines = f.readlines()
	print(len(lines))

    for i in range(1, len(lines)):
        segment = lines[i].rstrip().split(",")
        id = str(segment[1])
        name = str(segment[3])
        windIDs[id] = name
        print(windIDs, len(windIDs))

	# read gpsfile to get all wind county+id link to ID


	# fetch wind data for a round (csv)-query DB
	result = client.query('select * from wind where time > now() - 1h order by time DESC limit 1;')
	# query = client.query('select * from wind where time > now() - 1h  group by "Device_id" order by time DESC limit 1;')
	print(result)


    if __name__ == '__main__':
       main()