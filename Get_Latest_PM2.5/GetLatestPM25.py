import sys
import re
import os
import json
import time
import csv


from influxdb import InfluxDBClient
connectDB='PM25'
client = InfluxDBClient('localhost', 8086, 'root', 'root', connectDB) 
client.create_database(connectDB) 


from datetime import datetime
from pytz import timezone



#open a file for each airbox and write each data of the airbox to that file
storeLoc='/var/www/html/LASS/data/csv'
if not os.path.exists(storeLoc):
    os.makedirs(storeLoc)


#Get time list
def getTimeList(PM25Query,timeList):

    timeSet = " ".join(re.findall("u'time': u'(.*?)'", str(PM25Query)))
    timetemp=timeSet.split(' ')

    for j in range(len(timetemp)):
        timeList.append(timetemp[j])


#get a list of PM2.5 if PM2.5 
def getIDList(arg_measurement,IDList):
    if arg_measurement=='airbox' or arg_measurement=='lass':
        PM25Query = client.query(' select "PM2.5" from ' + arg_measurement + ' where time > now() - 1h group by "Device_id" order by time DESC limit 1;')    

        #extract ID from query replies
        IDSet = " "
        
        IDSet = " ".join(re.findall("\{u'Device_id': u'(.*?)'\}", str(PM25Query)))


        temp=IDSet.split(' ')
        for i in range(len(temp)):
            IDList.append(temp[i])

        return PM25Query

    else:
        print('Invalid Measurement.')
        return 1

#to count how many airbox device don't have the requested data


#get PM2.5 latest data
def getPM25List(PM25Query,PM25List):
    PM25Set = " ".join(re.findall("u'PM2.5':(.*?),", str(PM25Query)))
    

    PM25Set=PM25Set.strip()
   

    PM25temp=PM25Set.split('  ')

    for n in range(len(PM25temp)):
        PM25List.append(PM25temp[n])

# write the latest PM2.5 ,ID and time to csv file
def write2file(arg_measurement,IDList,PM25List,timeList):
    
    # read all posision in json
    with open('gpsfile.json') as data_file:    
        data = json.load(data_file)   
    allposition = data["sites"]

    # read all county/city in json
    with open('county.json', 'r') as readfile:
        countyTable = json.load(readfile)
    print(len(countyTable))

    # convert time zone to UTC+8
    for i in range(len(timeList)):
        datetime_object = datetime.strptime(timeList[i], '%Y-%m-%dT%H:%M:%SZ')
    
        datetime_object = datetime_object.replace(tzinfo=timezone('UTC'))
        now_zone = datetime_object.astimezone(timezone('Asia/Taipei'))
        timeList[i] =  now_zone.strftime('%Y-%m-%d (%H:%M:%S)')


    if(len(IDList)!=0):

        fp = open(storeLoc+"/"+arg_measurement+".csv", "w+")

        fp.write("device_id,pollution,timestamp,lat,lon,county/city\n")
        for IDindex in range(len(IDList)):

            # search position
            pos = ("","")
            for element in allposition:
                if element['id'] == str(IDList[IDindex]):
                    pos = (str(element['lat']), str(element['lon']))
    
                    break

            # search county/city
            for k in countyTable:
                if IDList[IDindex] in countyTable[k][arg_measurement]:
                    belongArea = k

            fp.write( str(IDList[IDindex])+","+str(PM25List[IDindex])+","+timeList[IDindex]+","+str(pos[0])+","+str(pos[1])+","+str(belongArea)+"\n");

        fp.close()

def main():

        #read in target measurement
        arg_measurementList = ['airbox','lass']
         #get a list of distinct ID
        IDList=[]
        timeList=[]
        PM25List=[]

        #get latest PM2.5 data and store it in CSV files from DB every 5 mins
        while(True):
            
            # re generate all position for lass, airbox, factory, windsite
            os.system('python region_graph.py')
            
            # re classify to city/county
            os.system('python classify/classify.py')


            for mIndex in range(len(arg_measurementList)):
                #get all IDs in this measurement
                PM25Query=getIDList(arg_measurementList[mIndex],IDList)
                #Get PM2.5 list
                getPM25List(PM25Query,PM25List)
                #Get time list
                getTimeList(PM25Query,timeList)

                #write latest PM2.5 data to csv file
                write2file(arg_measurementList[mIndex],IDList,PM25List,timeList)

            
                print('Measurement: ',arg_measurementList[mIndex])
                print('Total responsive AirBox num(which has data in the past one hour): ',len(IDList))

                #clear Lists before containing data from other measurement
                del IDList[:]
                del timeList[:]
                del PM25List[:]
            #get latest PM2.5 data from DB every 5 mins
            print("sleeping")
            time.sleep(300)
            print("wake up")
                
if __name__ == '__main__':
            main()

