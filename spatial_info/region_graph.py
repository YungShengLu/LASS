'''
* The program will query data in the DB, output a graph with nodes and links.
* Output JSON file?

* Nodes has different types(lass/airbox/factory)
'''
class Nodes(object):
	def __init__(self, id, type, lon, lat):
		super(Nodes, self).__init__()
		self.id = id
		self.type = type
		self.lon = lon
		self.lat = lat
	def hello():
		print("I'm "+ id)


def main():
	f = open("data.csv", 'r')
	lines = f.readlines()
	print(len(lines))

# fuction: compute distance given lon, lat
def compute_dis(lon, lat):
	pass
if __name__ == '__main__':
	main()