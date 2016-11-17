import sys
import re
from influxdb import InfluxDBClient
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'AirBox_test') 
client.create_database('AirBox_test') 

#extract ID from query replies
def getIDList(IDList,arg_city):
	#get all device id
	result = client.query(' select "PM2.5"::field,"Device_id"::tag  from '+ arg_city +' group by "Device_id" limit 1;') 
	#print("Result: {0}".format(result)) 

	#extract ID from query replies
	IDSet = " ".join(re.findall("74[0-9A-Z]\w+|28[0-9A-Z]\w+", str(result)))
	temp=""
	for index in range(len(IDSet)):
		if index%26==0:
			temp+=IDSet[index:index+12]
			IDList.append(temp)
			temp=""

#get a list of PM2.5 if PM2.5 ranges from 10~99
def getPM25List(PM25List,arg_city,IDList,IDindex):
	PM25Query = client.query(' select "PM2.5" from ' + arg_city + ' where "Device_id"=\''+IDList[IDindex]+'\';') 	
	PM25Set = " ".join(re.findall("(?:\d*)?\d,", str(PM25Query)))
	PM25temp=""
	for index in range(len(PM25Set)):
		if index%4==0:
			PM25temp+=PM25Set[index:index+2]
			PM25List.append(PM25temp)
			PM25temp=""	

#open a file for each airbox and write each data of the airbox to that file
def write2file(arg_city,IDList,IDindex,PM25List):
	fp = open("../timeFactorObservation/"+arg_city+"/"+IDList[IDindex]+".csv", "w+")
	for PM25index in range(len(PM25List)): 
		fp.write( str(PM25index)+","+PM25List[PM25index]+"\n");
				#print (str(PM25index)+","+PM25List[PM25index]+"\n")

				#print (arg_city.capitalize()+" Finish time: "+str(finish_time), end="\n", file=fp)
	        	
	fp.close()

def main():

	#read in target city
	arg_city = sys.argv[1].capitalize()

	#get a list of distinct ID
	IDList=[]
	getIDList(IDList,arg_city)
	

	print('City: ',arg_city)
	print('IDList: ',IDList)
	print('AirBox num: ',len(IDList))

	# get data from each airbox and write it to each airbox's csv file
	for IDindex in range(len(IDList)): 
		#get a list of PM2.5 if PM2.5 ranges from 10~99
		PM25List=[]
		getPM25List(PM25List,arg_city,IDList,IDindex)

		#write to file	
		write2file(arg_city,IDList,IDindex,PM25List)
		

if __name__ == '__main__':
        main()

