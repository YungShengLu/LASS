# Split ids to Taiwan by each county.
# input: gpsfile.json(in /home/ikdd/execute/Get_Latest_PM2.5), output.json(polygon), county.json(queried before)
# output: county.json(contain factory, lass, airbox)
# Use 2 methods: shapely polygon, google map api

import json
from shapely.geometry import shape, Point
import urllib

## Note: the path is from the caller, that is, the outer layer(classify outside)

# record all gps location
with open('gpsfile.json', 'r') as readfile:
	gps = json.load(readfile)
print(len(gps["sites"]))

# record Taiwan county polygon
taiwan = []
with open('classify/output.json', 'r') as readfile:
	county = json.load(readfile)
print(len(county["features"]))

for area in county["features"]:
	taiwan.append(area["properties"]["COUNTYENG"])
print(taiwan)

# load data that has been queried before to reduce API usages
try:
	with open('county.json', 'r') as readfile:
		countyTable = json.load(readfile)
	print(len(countyTable))
except IOError:
	print("no county.json")
	countyTable = {}

def main():

	# use 2 methods to identify which county:
	# main is google api, polygon methods is to support
	
	county2id  = countyTable	# county2id will "write" to json
	exceptList = []				# the first time that google api can't process
	addingId   = []				# id that not in queried before file, so try google api first
	UsePolygonList = [] 		# try by polygon methods
	
	
	# find the adding id
	exist = []
	for c in countyTable:
		for type in countyTable[c]:
			for each in countyTable[c][type]:
				exist.append(each)
	print(len(exist), len(gps["sites"]))
	for sites in gps["sites"]:
		if sites["id"] not in exist:
			addingId.append(sites["id"])
	print(addingId)

	# the first time, google api all
	if county2id == {}:
		UseGoogleApiAll(county2id, exceptList)
		print("finish google map")
		print("first google api remain", exceptList)
		addingId = exceptList
	# google api the rest
	UsePolygonList = UseGoogleApiRest(addingId, county2id)
	print("ready to use polygon method", UsePolygonList)
	
	# method2
	UsePolygon(county2id, UsePolygonList)
	print("finish shapely")

	# write to json format
	with open('county.json', 'w') as writefile:
		json.dump(county2id, writefile, indent=4)
	print(UsePolygonList)

	# # Using county.json
	# with open('county.json', 'r') as readfile:
	# 	locations = json.load(readfile)
	# for k in locations.keys():
	# 	print(k)

def UseGoogleApiAll(county2id, exceptList):
	county2id["Foreign"] = {"factory":[],"lass":[],"airbox":[], "wind":[]}

	for t in taiwan:
		county2id[t] = {"factory":[],"lass":[],"airbox":[], "wind":[]}
	# Use GoogleApi as main tool, and if can,t handle, append to exceptList then handle later
	failcount = {}		# id: failcount

	# for i in range(len(gps["sites"])):
	i = 0
	while i < len(gps["sites"]):
	# while i < 100:
		lat = str(gps["sites"][i]["lat"])
		lon = str(gps["sites"][i]["lon"])
		type = gps["sites"][i]["type"]
		id = gps["sites"][i]["id"]

		if id not in failcount:
			failcount[id] = 0

		# google api can't get data
		if failcount[id] >= 5:
			exceptList.append(id)
			print(i+1, "always no result")
			i += 1
			# try several times but no results
			continue

		# google map api
		url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+"%2C"+lon+"&key=AIzaSyCsfSh8Gmn-8uW07dIxoTvgE0xXPlIL0d8"
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		print(id)
		# print(data["results"][0]["address_components"][3]["long_name"])
		try:
			succeed = 0

			for j in reversed(data["results"][0]["address_components"]):
				# print(j["types"])

				if "administrative_area_level_" in j["types"][0]:
					result = j["long_name"]
					print(i+1, id, result)
					if result in taiwan:
						if result not in county2id:
							county2id[result] = {"factory":[],"lass":[],"airbox":[],"wind":[]}
						county2id[result][type].append(id)
					else:
						county2id["Foreign"][type].append(id)
					i += 1
					succeed = 1
					break
				# string = str(j["types"])
				# print((string))
			if succeed == 0:
				i += 1
				print(i+1, "no administrative_area_level_")
				county2id["Foreign"][type].append(id)

		except IndexError as e:
			print (e)
			print(i+1, "can't find")
			failcount[id] += 1


def UseGoogleApiRest(addingId, county2id):
	
	remain = list(addingId)		# remain to polygon method
	print("precess some of id by api")
	print(addingId)

	failcount = {}		# id: failcount
	i = 0
	while i < len(gps["sites"]):
		lat = str(gps["sites"][i]["lat"])
		lon = str(gps["sites"][i]["lon"])
		type = gps["sites"][i]["type"]
		id = gps["sites"][i]["id"]
		# only want not has been queried
		if id not in addingId:
			i += 1
			continue
		
		if id not in failcount:
			failcount[id] = 0

		# google api can't get data
		if failcount[id] >= 5:
			# exceptList.append(id)
			print(i+1, "always no result")
			i += 1
			# try several times but no results
			continue

		# google map api
		url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+"%2C"+lon+"&key=AIzaSyCsfSh8Gmn-8uW07dIxoTvgE0xXPlIL0d8"
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		print(id)

		try:
			succeed = 0

			for j in reversed(data["results"][0]["address_components"]):

				if "administrative_area_level_" in j["types"][0]:
					result = j["long_name"]
					print(i+1, id, result)
					if result in taiwan:
						if result not in county2id:
							county2id[result] = {"factory":[],"lass":[],"airbox":[]}
						county2id[result][type].append(id)
						remain.remove(id)
					else:
						county2id["Foreign"][type].append(id)
						remain.remove(id)
					i += 1
					succeed = 1
					break

			if succeed == 0:
				i += 1
				print(i+1, "no administrative_area_level_")
				county2id["Foreign"][type].append(id)
				remain.remove(id)

		except IndexError as e:
			print (e)
			print(i+1, "can't find")
			failcount[id] += 1

	return remain

def UsePolygon(county2id, UsePolygonList):

	for i in range(len(gps["sites"])):
		lat = gps["sites"][i]["lat"]
		lon = gps["sites"][i]["lon"]
		type = gps["sites"][i]["type"]
		id = gps["sites"][i]["id"]

		if id not in UsePolygonList:
			continue
		
		point = Point(lon, lat)

		for area in county["features"]:
			# whichcounty = area["properties"]["COUNTYENG"]
			# print(whichcounty)
			canfind = 0
			polygon = shape(area["geometry"])
			# print(polygon)
			if polygon.contains(point):
				print("contain")
				whichcounty = area["properties"]["COUNTYENG"]
				canfind = 1
				break
			# else:
			# 	print("not contains")
		if canfind:
			print(id, whichcounty, i+1)
			if whichcounty not in county2id:
				county2id[whichcounty] = {"factory":[],"lass":[],"airbox":[],"wind":[]}
			county2id[whichcounty][type].append(id)
			UsePolygonList.remove(id)
		else:
			print("can not classify", i+1)
			# county2id["Foreign"][type].append(id)

	# print(lat, lon, type, id)

if __name__ == '__main__':
	main()

