import sys
import re
from influxdb import InfluxDBClient
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'AirBox_test') 
client.create_database('AirBox_test') 
PM25List=[]
GPSList=[]
timeList=[]
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
def getPM25List(PM25List,arg_city,IDList,IDindex,timeList):
	PM25Query = client.query(' select "PM2.5" from ' + arg_city + ' where "Device_id"=\''+IDList[IDindex]+'\';') 	
	#print PM25Query
	PM25Set = " ".join(re.findall("(?:\d*)?\d,", str(PM25Query)))
	#print PM25Set
	
	#print ('pm25 len ',len(PM25Set))
	
	# split PM25Set by ',' to create a list to retain all PM2.5 value
	PM25List=PM25Set.split(',')

	#delete the empty element derived from the last ',' in PM25Set at the end of this list
	del PM25List[len(PM25List)-1]
	
	#write pm2.5 to file	
	write2file(arg_city,IDList,IDindex,PM25List,timeList)
      

	
#open a file for each airbox and write each data of the airbox to that file
def write2file(arg_city,IDList,IDindex,PM25List,timeList):
	fp = open("../timeFactorObservation/"+arg_city+"/"+IDList[IDindex]+".csv", "w+")
	#print len(timeList)
	for PM25index in range(len(PM25List)): 
		fp.write( str(PM25index)+","+PM25List[PM25index]+","+timeList[PM25index]+"\n");
				#print (str(PM25index)+","+PM25List[PM25index]+"\n")

				#print (arg_city.capitalize()+" Finish time: "+str(finish_time), end="\n", file=fp)
	        	
	fp.close()




#get a list of PM2.5 if PM2.5 ranges from 10~99
def getGPS_TimeList(GPSList,arg_city,IDList,IDindex):

	

	#get Lon
	GPSQuery = client.query(' select "Gps_lon" from ' + arg_city + ' where "Device_id"=\''+IDList[IDindex]+'\';') 	
	GPSLonSet = re.search("(?:\d+\.\d*)?\d,", str(GPSQuery))
	
	#get Lat
	GPSQuery = client.query(' select "Gps_lat" from ' + arg_city + ' where "Device_id"=\''+IDList[IDindex]+'\';') 	
	GPSLatSet = re.search("(?:\d+\.\d*)?\d,", str(GPSQuery))
	GPSList.append('Lon: '+GPSLonSet.group().replace(',','')+','+'Lat: '+GPSLatSet.group().replace(',',''))
	
	#get time
	timeSet = " ".join(re.findall("\d{4}[-]?\d{2}[-]?\d{2}T\d{2}[:]?\d{2}[:]?\d{2}Z", str(GPSQuery)))
	#print timeSet
	timeList=timeSet.split(' ')
	#print timeList
	
	return timeList
	


	
def writeGPS2file(arg_city,IDList,GPSList):
	fp = open("../timeFactorObservation/"+arg_city+"/GPSList.csv", "w+")
	for GPSindex in range(len(GPSList)): 
		fp.write( IDList[GPSindex]+","+GPSList[GPSindex]+"\n");
				
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
		timeList=getGPS_TimeList(GPSList,arg_city,IDList,IDindex)
		
		#get PM25List and write to file	
		getPM25List(PM25List,arg_city,IDList,IDindex,timeList)
		#print PM25List  is empty here
		
	
	
	#write GPS and ID to file
	writeGPS2file(arg_city,IDList,GPSList)
if __name__ == '__main__':
        main()

