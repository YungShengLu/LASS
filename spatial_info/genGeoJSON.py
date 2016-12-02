from json import dump, load
from re import compile
import sys


class genGeoJSON:
	def __init__(self, filename):
		self.filename = filename
		self.data = {}
		self.json_factory = {
			'type': 'FeatureCollection',
			'features': []
		}
		self.json_airbox = {
			'type': 'FeatureCollection',
			'features': []
		}
		self.json_lass = {
			'type': 'FeatureCollection',
			'features': []
		}

	def readJSON(self):
		with open(self.filename) as file:
			self.data = load(file)
		self.createJSON()

	def createJSON(self):
		for key in self.data['sites']:
			if key['type'] == 'factory':
				self.json_factory['features'].append({
					'type': 'Feature',
					'geometry': {
						'type': 'Point',
						'coordinates': [key['lon'], key['lat']]
					},
					'properties': {
						'device_id': key['id'],
						'type': key['type']
					}
				})
			elif key['type'] == 'airbox':
				self.json_airbox['features'].append({
					'type': 'Feature',
					'geometry': {
						'type': 'Point',
						'coordinates': [key['lon'], key['lat']]
					},
					'properties': {
						'device_id': key['id'],
						'type': key['type']
					}
				})
			elif key['type'] == 'lass':
				self.json_lass['features'].append({
					'type': 'Feature',
					'geometry': {
						'type': 'Point',
						'coordinates': [key['lon'], key['lat']]
					},
					'properties': {
						'device_id': key['id'],
						'type': key['type']
					}
				})

		#generate GeoJSON file
		self.generateJSON('factory', self.json_factory)
		self.generateJSON('airbox', self.json_airbox)
		self.generateJSON('lass', self.json_lass)

	def generateJSON(self, src, data):
		with open('GeoJSON/' + src + '_geo.json', 'w') as outfile:
			dump(data, outfile)


def main():
	#load origin JSON file.
	filename = sys.argv[1]

	json = genGeoJSON(filename)
	json.readJSON()


if __name__ == '__main__':
	main()