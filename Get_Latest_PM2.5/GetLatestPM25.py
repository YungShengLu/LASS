import sys
import re
import os
import json
import time

from influxdb import InfluxDBClient
connectDB='PM25'
client = InfluxDBClient('localhost', 8086, 'root', 'root', connectDB) 
client.create_database(connectDB) 





#open a file for each airbox and write each data of the airbox to that file
if not os.path.exists("/var/www/html/Demo/csv/"):
    os.makedirs("/var/www/html/Demo/csv/")


#Get time list
def getTimeList(PM25Query,timeList):

    timeSet = " ".join(re.findall("u'time': u'(.*?)'", str(PM25Query)))
    timetemp=timeSet.split(' ')

    for j in range(len(timetemp)):
        timeList.append(timetemp[j])



#get a list of PM2.5 if PM2.5 
def getIDList(arg_measurement,IDList):
    if arg_measurement=='airbox' or arg_measurement=='lass':
        PM25Query = client.query(' select "PM2.5" from ' + arg_measurement + ' group by "Device_id" order by time DESC limit 1;')    
        
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





#write the latest PM2.5 ,ID and time to csv file
def write2file(arg_measurement,IDList,PM25List,timeList):
        
    if(len(IDList)!=0):

        fp = open("/var/www/html/Demo/csv/"+arg_measurement+".csv", "w+")
        for IDindex in range(len(IDList)):

            fp.write( str(IDList[IDindex])+","+str(PM25List[IDindex])+","+timeList[IDindex]+"\n");

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
                print('Total AirBox num: ',len(IDList))

                #clear Lists before containing data from other measurement
                del IDList[:]
                del timeList[:]
                del PM25List[:]
            #get latest PM2.5 data from DB every 5 mins
            time.sleep(300)
                
        
        
        
if __name__ == '__main__':
            main()

