'''
* The program will query data in the DB, output a graph with nodes and links.
* Output JSON file?

* Nodes has different types(lass/airbox/factory)
'''
class Node(object):
    def __init__(self, id, type, lat, lon):
        super(Node, self).__init__()
        self.id = id
        self.type = type
        self.lat = lat
        self.lon = lon
    def hello(self):
        print("I'm "+ self.id+" Lat="+self.lat+" and Lon="+self.lon)


def main():
    Allnodes = []                      # a dictionary store all nodes
    # 1. read factory files and construre a graph
    type = "factory"
    f = open("data.csv", 'r')
    lines = f.readlines()
    print(len(lines))
    # Get all factories
    # use "factoryXXX" as id
    for i in range(1, len(lines)):
        segment = lines[i].split(",")
        id = "factory" + segment[0]
        lat = segment[1]
        lon = segment[2]
        print([id, type, lat, lon])
        
        node = Node(id, type, lat, lon)
        node.hello()
        Allnodes.append(node)
        # testing
        #p1 = (120.734, 24.12)
        #p2 = (121.535, 25.023)
        #print(compute_dis(p1[0],p1[1],p2[0],p2[1]))
   	for n in Allnodes:
   		n.hello() 


# fuction: compute distance given lon, lat
from math import radians, cos, sin, asin, sqrt
def compute_dis(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371    # earth radius
    return c * r * 1000         # The units is "meter"

if __name__ == '__main__':
    main()
