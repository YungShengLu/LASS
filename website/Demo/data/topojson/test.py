from json import dump, load
import csv
import sys


class genCSV:
	def __init__(self):
		self.filenames = ['factory_topo.json', 'lass_topo.json', 'airbox_topo.json']
		self.data = {}
		self.device_id = []

	def createCSV(self):
		for name in self.filenames:
			with open(name, 'r') as file:
				self.data = load(file)

			for key in self.data['objects']['collection']['geometries']:
				self.device_id.append(key['properties']['device_id'])
			#print(key['properties']['device_id'])

			with open('test.csv', 'w') as file:
				w = csv.writer(file)
				w.writerow(self.device_id)

def main():
	json = genCSV()
	json.createCSV()

if __name__ == '__main__':
	main()