'''
* The program will query data in the DB, output a graph with nodes and links.

* Output JSON file?

* example(bigger nodes):
Taipei: {<id1>, <id2>...}
Kaohsiung: {<id3>, <id4>}

* example(smaller node, with distance):
{id1: {id2:13, id3:16, id4:18}}
{id2: {id1:13, id6:19}}....

'''
# recursivily find all files
import os	

def main():
	cyties = []
	for city in os.listdir("../PM25_analysis_tool/timeFactorObservation"):
		print(city)
		cyties.append(city)
	print("use list to get all GPSlist graph")
	
	big_node = {}				
	small_node = {}	
	locations = {}	

	# open GPS files in each city's folder
	for city in cyties:
		big_node[city] = []
		GPSs = open("../PM25_analysis_tool/timeFactorObservation/"+city+"/GPSList.csv", 'r')
		
		print("print"+city)

		content = GPSs.readlines()

		
		for data in content:
			data = data.rstrip()		# remove '\n'
			print(data)
			data = data.split(',')		# split by ',' to get all attribute
			print(data)
			id = data[0]
			lon = data[1]				# longitude
			lat = data[2]				# latitude
			print(id,lon,lat)

			# add to graph
			big_node[city].append(id)
			small_node[id] = {}			# graph: based on distance
			locations[id] = (lon, lat)


		print(len(content))
		print()
	print(big_node,len(big_node))
	print(small_node,len(small_node))
	print(locations,len(locations))

# fuction: compute distance given lon, lat
def compute_dis(lon, lat):
	pass
if __name__ == '__main__':
	main()