from requests import get, exceptions
from progressbar import ProgressBar, Bar, Percentage
from time import sleep
from influxdb import InfluxDBClient
import sys


class parseSite:
	def __init__(self, city, siteID, database):
		self.parseCity = city
		self.parseSite = siteID
		self.url = 'http://nrl.iis.sinica.edu.tw/LASS/last.php?device_id='
		self.jsonData = {}
		#connect with DB (AirBox / AirBox_test)
		self.database = database
		self.client = InfluxDBClient('localhost', 8086, 'root', 'root', self.database)
		self.client.create_database(database)

	def parseData(self):
		count = 12	#test

		print('>>> Parse site data: ' + self.parseCity.capitalize())
		progress = ProgressBar(maxval = self.parseSite['siteNum'], widgets = [Bar('=', '[', ']'), ' ', Percentage()]).start()
		self.jsonData = {}

		for ID, perc, i in zip(self.parseSite['id'], range(self.parseSite['siteNum']), range(count)):
			try:
				req = get(self.url + ID, timeout = 25)
			except exceptions.Timeout as e:
				print('Site cannot connect: ' + ID)
				continue

			self.jsonData = req.json()

			'''if self.jsonData.get('app') is None:
				self.jsonData.update({'app': 'N/A'})
			if self.jsonData.get('gps_lat') is None:
				self.jsonData.update({'gps_lat': -1.0})
			if self.jsonData.get('gps_lon') is None:
				self.jsonData.update({'gps_lon': -1.0})
			if self.jsonData.get('gps_num') is None:
				self.jsonData.update({'gps_num': -1})
			if self.jsonData.get('s_t0') is None:
				self.jsonData.update({'s_t0' : -1.0})
			if self.jsonData.get('s_h0') is None:
				self.jsonData.update({'s_h0': -1})
			if self.jsonData.get('s_d0') is None:
				self.jsonData.update({'s_d0': -1})
			if self.jsonData.get('s_d1') is None:
				self.jsonData.update({'s_d1': -1})
			if self.jsonData.get('s_d2') is None:
				self.jsonData.update({'s_d2': -1})'''
			if self.jsonData.get('s_d0') is None:
				continue

			progress.update(perc + 1)
			sleep(0.1)

			json_body = [{
				"measurement": self.parseCity.capitalize(),
				"tags": {
					"Device_id": self.jsonData.get('device_id')
				},
				"time": self.jsonData.get('timestamp'),
				"fields":{
					"PM2.5":self.jsonData.get('s_d0'),
					"s_d1": self.jsonData.get('s_d1'),
					"s_d2": self.jsonData.get('s_d2'),
					"Temperature":float(self.jsonData.get('s_t0')),
					"Humidity": self.jsonData.get('s_h0'),
					"Gps_lat": float(self.jsonData.get('gps_lat')),
					"Gps_lon": float(self.jsonData.get('gps_lon')),
					"Gps_num": self.jsonData.get('gps_num'),
					"app": self.jsonData.get('app')
				}
			}]
			self.client.write_points(json_body)
		progress.finish()
