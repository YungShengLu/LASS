import sys
import re
import os
import json
import ast
import shutil


from influxdb import InfluxDBClient
connectDB='PM25'
client = InfluxDBClient('localhost', 8086, 'root', 'root', connectDB) 
client.create_database(connectDB) 





#open a file for each airbox and write each data of the airbox to that file
if not os.path.exists("./Latest_PM2.5"):
    os.makedirs("./Latest_PM2.5")


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

        fp = open("./Latest_PM2.5/"+arg_measurement+".csv", "w+")
        for IDindex in range(len(IDList)):

            fp.write( str(IDList[IDindex])+","+str(PM25List[IDindex])+","+timeList[IDindex]+"\n");

        fp.close()







def main():

        #read in target measurement
        arg_measurement = sys.argv[1]
         #get a list of distinct ID
        IDList=[]
        timeList=[]
        PM25List=[]

       


        #get all IDs in this measurement
        PM25Query=getIDList(arg_measurement,IDList)
        #Get PM2.5 list
        getPM25List(PM25Query,PM25List)
        #Get time list
        getTimeList(PM25Query,timeList)

        #write latest PM2.5 data to csv file
        write2file(arg_measurement,IDList,PM25List,timeList)

        


        print('Measurement: ',arg_measurement)
        print('Total AirBox num: ',len(IDList))
        
        
        
if __name__ == '__main__':
            main()

