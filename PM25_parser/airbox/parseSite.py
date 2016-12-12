from requests import get, exceptions
from time import sleep, gmtime, strftime
from influxdb import InfluxDBClient
###
from datetime import datetime
####


class parseSite:
    def __init__(self, src, database):
        self.src = src
        self.url = 'http://nrl.iis.sinica.edu.tw/LASS/last-all-' + self.src + '.json'
        self.jsonData = {}
        #connect with DB (PM25)
        self.database = database

        
    def parseData(self):
        #connect with DB (PM25)
        self.client = InfluxDBClient('localhost', 8086, 'root', 'root', self.database)
        self.client.create_database(self.database)

        try:
            req = get(self.url, timeout = 25)
        except exceptions.Timeout as e:
            print('Website cannot connect: ' + self.url)

        #parse data
        self.jsonData = req.json()



        #classify the data and write into database
        for i in range(self.jsonData.get('num_of_records')):
            
            # fill -1 to attrubute if no values
            pm25 = self.jsonData.get('feeds')[i].get('s_d0')
            print(pm25, type(pm25))
            if pm25 == 'NaN' or pm25 == None:
                continue


            temperature = self.jsonData.get('feeds')[i].get('s_t0')  
            print(temperature)
            if temperature is None:
                temperature = -1

            
            humidity = self.jsonData.get('feeds')[i].get('s_h0')  
            if humidity is None:
                humidity = -1
            
            json_body = [{
                "measurement":self.src,
                #"time": self.jsonData.get('version'),
                "time":self.jsonData.get('version'),
                "tags": {
                    "Device_id": self.jsonData.get('feeds')[i].get('device_id')
                },
                "fields": {
                    "PM2.5": float(pm25),
                    "Temperature": float(temperature),
                    "Humidity": float(humidity),
                    "Gps_lat": float(self.jsonData.get('feeds')[i].get('gps_lat')),
                    "Gps_lon": float(self.jsonData.get('feeds')[i].get('gps_lon')),
                    "Gps_num": self.jsonData.get('feeds')[i].get('gps_num')
                }
    
            }]
            self.client.write_points(json_body)

        #parse record
        self.record()

    def record(self):
        #connect with DB (AirBox_record / LASS_record)
        originalDB=self.database
        self.database = 'AirBox_record'
        self.client = InfluxDBClient('localhost', 8086, 'root', 'root', self.database)
        self.client.create_database(self.database)

        json_body = [{
            "measurement": self.src + '_record',
            #"time": strftime("%Y-%m-%d_%H:%M:%S", gmtime()),
            "time":datetime.utcnow(),

            "tags": {
                "Parse_time": self.jsonData.get('version')
            },
            "fields": {
                "Parse_site": self.jsonData.get('num_of_records'),
                "Parse_src": self.jsonData.get('source')
            }
        }]
        self.client.write_points(json_body)

        #restore self.database to the DB that stores the parsed data.
        self.database=originalDB


