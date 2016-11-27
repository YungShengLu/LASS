from requests import get, exceptions
from time import sleep, gmtime, strftime
from influxdb import InfluxDBClient


class parseSite:
	def __init__(self, src, database):
		self.src = src
		self.url = 'http://nrl.iis.sinica.edu.tw/LASS/last-all-' + self.src + '.json'
		self.jsonData = {}

		#connect with DB (AirBox / LASS)
		self.database = database
		self.client = InfluxDBClient('localhost', 8086, 'root', 'root', self.database)
		self.client.create_database(database)

	def parseData(self):
		try:
			req = get(self.url, timeout = 25)
		except exceptions.Timeout as e:
			print('Website cannot connect: ' + self.url)

		#parse data
		self.jsonData = req.json()

		#classify the data and write into database
		for i in range(self.jsonData.get('num_of_records')):
			json_body = [{
				"time": self.jsonData.get('version'),
				"fields": {
					"device_id": self.jsonData.get('feeds')[i].get('device_id'),
					"PM2.5": self.jsonData.get('feeds')[i].get('s_d0'),
					"Temperature": float(self.jsonData.get('feeds')[i].get('s_t0')),
					"Humidity": self.jsonData.get('feeds')[i].get('s_h0'),
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
		self.database = 'AirBox_record'
		self.client = InfluxDBClient('localhost', 8086, 'root', 'root', self.database)
		self.client.create_database(database)

		json_body = [{
			"time": strftime("%Y-%m-%d_%H:%M:%S", gmtime()),
			"fields": {
				"parse_time": self.jsonData.get('version'),
				"parse_site": self.jsonData.get('num_of_records'),
				"parse_src": self.jsonData.get('source')
			}
		}]
		self.client.write_points(json_body)
