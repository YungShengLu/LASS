# -*- coding: UTF-8 -*-

# fetch wind data each hour
import sys
import re
import os
import json
import time
import csv

import codecs

from influxdb import InfluxDBClient
import uniout

from datetime import datetime
from pytz import timezone

connectDB='LASS_WIND'
client = InfluxDBClient('localhost', 8086, 'root', 'root', connectDB) 
client.create_database(connectDB) 

storeLoc='/var/www/html/LASS/data/csv/curentWind.csv'


def main():

    # read wind location csv to link id to name
    windIDs = {}       #{id: (county/city,name,lat,lon)}
    f = open("wind_location.csv", 'r')
    lines = f.readlines()
    print(len(lines))

    for i in range(1, len(lines)):
        segment = lines[i].rstrip().split(",")
        
        id = str(segment[1])
        county = str(segment[2])
        name = str(segment[3])
        lat = str(segment[4])
        lon = str(segment[5])

        windIDs[id] = (county, name, lat, lon)


    while 1:
        
        # read gpsfile to get all wind county+id link to ID
        print("screen program: 1 hour write wind data to csv")
        queryNowWind(windIDs)

        print("sleep")
        time.sleep(3600)

def queryNowWind(windIDs):
    print("query")
    
    f = codecs.open(storeLoc, "w",encoding="utf-8")

    writer = csv.writer(f)
    writer.writerow(["id", "time", "name", "county/city", "lat", "lon", "direction", "speed(m/s)"])

    # fetch wind data for a round (csv)-query DB
    for id in windIDs:

        name = windIDs[id][1].decode('utf-8')
        county = windIDs[id][0].decode('utf-8')
        lat = windIDs[id][2]
        lon = windIDs[id][3]

        # querying
        want ='select Direction,Speed from wind where Station='+'\''+name+'\''+' and time > now() - 1h order by time DESC limit 1;'

        result = str(client.query(want))


        # re matching
        direction = re.findall( "Direction': u'(.*?)',", result)[0].decode('unicode-escape')
        speed = re.findall( "Speed': u'(.*?)',", result)[0]
        timestamp = re.findall( "time': u'(.*?)\.", result)[0]

        # process time to taiwan zone
        # print(timestamp)
        datetime_object = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
    
        datetime_object = datetime_object.replace(tzinfo=timezone('UTC'))
        now_zone = datetime_object.astimezone(timezone('Asia/Taipei'))
        timestamp =  now_zone.strftime('%Y-%m-%d (%H:%M:%S)')


        
        f.write((id)+","+(timestamp)+","+(name)+","+(county)+","+(lat)+","+(lon)+","+(direction)+","+(speed)+"\n")
    f.close()


if __name__ == '__main__':
       main()

