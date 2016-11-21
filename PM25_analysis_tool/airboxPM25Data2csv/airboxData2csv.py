import sys
import re
import os
import json
import ast

from influxdb import InfluxDBClient
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'AirBox_test') 
client.create_database('AirBox_test') 
PM25List=[]
GPSList=[]
timeList=[]

#open a file for each airbox and write each data of the airbox to that file
if not os.path.exists("../timeFactorObservation"):
        os.makedirs("../timeFactorObservation")
if not os.path.exists("../timeFactorObservation/Taipei"):
		os.makedirs("../timeFactorObservation/Taipei")
if not os.path.exists("../timeFactorObservation/Newtaipei"):
		os.makedirs("../timeFactorObservation/Newtaipei")
if not os.path.exists("../timeFactorObservation/Taichung"):
		os.makedirs("../timeFactorObservation/Taichung")
if not  os.path.exists("../timeFactorObservation/Tainan"):
		os.makedirs("../timeFactorObservation/Tainan")
if not  os.path.exists("../timeFactorObservation/Kaohsiung"):
		os.makedirs("../timeFactorObservation/Kaohsiung")


#extract ID from query replies
def getIDList(IDList,arg_city):
        #get all device id
        result = client.query(' select "PM2.5"::field,"Device_id"::tag  from '+ arg_city +' group by "Device_id" limit 1;') 
       

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
        
        PM25Set = " ".join(re.findall('\[(.*?)\]', str(PM25Query)))

      

        tempPM25List=PM25Set.split('}, {')
        
        #due to the function of split() the first and the last element has { in the beginning and } in the end of the string reapectively.
        #To handle the above problem
        tempPM25List[0]=tempPM25List[0].replace('{','')
        tempPM25List[len(tempPM25List)-1]=tempPM25List[len(tempPM25List)-1].replace('}','')
        
        #string to dict and append PM2.5 value to PM2.5List
        for i in range(len(tempPM25List)): 
        	tempPM25List[i]="{"+tempPM25List[i]+"}"
        	data_PM25 = ast.literal_eval(tempPM25List[i])
        	PM25List.append(data_PM25['PM2.5'])
        
        

        



def write2file(arg_city,IDList,IDindex,PM25List,timeList):
        fp = open("../timeFactorObservation/"+arg_city+"/"+IDList[IDindex]+".csv", "w+")
        for PM25index in range(len(PM25List)): 
                fp.write( str(PM25index)+","+str(PM25List[PM25index])+","+timeList[PM25index]+"\n");
                                #print (str(PM25index)+","+PM25List[PM25index]+"\n")

                                #print (arg_city.capitalize()+" Finish time: "+str(finish_time), end="\n", file=fp)
                        
        fp.close()




#get a list of PM2.5 if PM2.5 ranges from 10~99
def getGPS_TimeList(GPSList,arg_city,IDList,IDindex):

        

        #get Lon
        GPSQuery = client.query(' select "Gps_lon" from ' + arg_city + ' where "Device_id"=\''+IDList[IDindex]+'\'limit 1;')    

        refine = re.findall('\[(.*?)\]', str(GPSQuery))[0]

        data_lon = ast.literal_eval(refine)
       



        #get Lat
        GPSQuery = client.query(' select "Gps_lat" from ' + arg_city + ' where "Device_id"=\''+IDList[IDindex]+'\';')   

        refine = re.findall('\[(.*?)\]', str(GPSQuery))[0]

        split = re.findall('\{(.*?)\}',refine)[0]
       
        new_string = "{"+split+"}"

        data_lat = ast.literal_eval(new_string)
       


        #append retrieved Lon and Lat to GPSList 
        GPSList.append(str(data_lon['Gps_lon'])+','+str(data_lat['Gps_lat']))
        
        #get time
        timeSet = " ".join(re.findall("\d{4}[-]?\d{2}[-]?\d{2}T\d{2}[:]?\d{2}[:]?\d{2}Z", str(GPSQuery)))
        timeList=timeSet.split(' ')
        
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
        	print("Retrieving data from "+str(IDList[IDindex]))
        	timeList=getGPS_TimeList(GPSList,arg_city,IDList,IDindex)
        	getPM25List(PM25List,arg_city,IDList,IDindex,timeList)
        	write2file(arg_city,IDList,IDindex,PM25List,timeList)
        	del PM25List[:]
        writeGPS2file(arg_city,IDList,GPSList)
if __name__ == '__main__':
        main()

