from requests import get
from progressbar import ProgressBar, Bar, Percentage
from time import sleep


class querySiteID:
	def __init__(self, city):
		self.queryCity = city
		self.url = 'http://nrl.iis.sinica.edu.tw/LASS/AirBox/'
		self.siteID = []
		self.siteNum = 0
		self.jsonData = {}

	def init(self):
		self.siteID = []
		self.siteNum = 0

	def queryID(self):
		progress = ProgressBar(maxval = len(self.queryCity), widgets = [Bar('=', '[', ']'), ' ', Percentage()]).start()

		for city, perc in zip(self.queryCity, range(len(self.queryCity))):
			try:
				req = get(self.url + city + '.json', timeout = 25)
			except exceptions.Timeout as e:
				print('City cannot connect: ' + city)
				continue

			data = req.json()
			self.init()

			for key1 in data.keys():
				if key1 == 'feeds':
					feeds = data[key1]
					for feed in feeds:
						for key2 in feed.keys():
							if key2 == 'site_id':
								self.siteID.append(feed[key2])
								self.siteNum += 1

			self.jsonData.update({
				city: {
					'siteNum': self.siteNum,
					'id': self.siteID
				}
			})

			progress.update(perc + 1)
			sleep(0.1)

		progress.finish()
		return self.jsonData