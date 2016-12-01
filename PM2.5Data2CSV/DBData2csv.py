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
PM25List=[]
#timeList=[]
#get a list of distinct ID
IDList=[]


#to count how many airbox device don't have the requested data
lackDataID=0

#open a file for each airbox and write each data of the airbox to that file
if not os.path.exists("./PM2.5_csv"):
        os.makedirs("./PM2.5_csv")
if not os.path.exists("./PM2.5_csv/lass"):
		os.makedirs("./PM2.5_csv/lass")
if not os.path.exists("./PM2.5_csv/airbox"):
		os.makedirs("./PM2.5_csv/airbox")





#get a list of PM2.5 if PM2.5 ranges from 10~99
def getIDList(arg_measurement,IDList):
        if arg_measurement=='airbox' or arg_measurement=='lass':
                PM25Query = client.query(' select "PM2.5" from ' + arg_measurement + ' group by "Device_id" limit 1;')    
               
                #extract ID from query replies
                IDSet = " "
                
                IDSet = " ".join(re.findall("\{u'Device_id': u'(.*?)'\}", str(PM25Query)))
                        
                       
                temp=IDSet.split(' ')
                for i in range(len(temp)):
                        IDList.append(temp[i])

        else:
                print('Invalid Measurement.')

#to count how many airbox device don't have the requested data
lackDataID=0
def getPM25List(PM25List,arg_measurement,IDindex,IDList,arg_pastTime):

        global lackDataID
        #Any variable assigned in a function is local to that function, unless it is specifically declared global. 
        
        #if user requests the history PM2.5 data in the past 1 hour in this ID 
        if len(sys.argv)==3 and arg_pastTime=='H':# found:
                
                PM25Query = client.query(' select "PM2.5" from ' + arg_measurement + ' where "Device_id" =\''+IDList[IDindex]+'\'  and time > now() - 1h;')       
                
                #check if the PM25 query result is empty,if yes,skip this one
                PM25Query=str(PM25Query)
                if PM25Query == 'ResultSet({})': 
                        print("Device_id: " +IDList[IDindex]+",no query result")
                        lackDataID=lackDataID+1
                        return


        #if user requests the history PM2.5 data in the past 24 hours in this ID 
        elif len(sys.argv)==3 and arg_pastTime=='D':# found:
                
                PM25Query = client.query(' select "PM2.5" from ' + arg_measurement + ' where "Device_id" =\''+IDList[IDindex]+'\'  and time > now() - 24h;')        

                #check if the PM25 query result is empty,if yes,skip this one
                PM25Query=str(PM25Query)
                if PM25Query == 'ResultSet({})': 
                        print("Device_id: " +IDList[IDindex]+",no query result")
                        lackDataID=lackDataID+1
                        return


        #if user requests the history PM2.5 data in the past 1 week in this ID 
        elif len(sys.argv)==3 and arg_pastTime=='W':# found:
                
                PM25Query = client.query(' select "PM2.5" from ' + arg_measurement + ' where "Device_id" =\''+IDList[IDindex]+'\'  and time > now() - 1w;')    
                
                #check if the PM25 query result is empty,if yes,skip this one
                PM25Query=str(PM25Query)
                if PM25Query == 'ResultSet({})': 
                        print("Device_id: " +IDList[IDindex]+",no query result")
                        lackDataID=lackDataID+1
                        return


        #if user requests all the history PM2.5 data in this ID 
        if len(sys.argv)==2:
                PM25Query = client.query(' select "PM2.5" from ' + arg_measurement + ' where "Device_id" =\''+IDList[IDindex]+'\';')    
      
        
        PM25Set = " ".join(re.findall('\[(.*?)\]', str(PM25Query)))

        
        PM25Set=PM25Set.replace('} {','}, {')
        
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
        

        



def write2file(arg_measurement,IDList,PM25List,IDindex):
        
        #if the device doesn't have the requested PM2.5 data,just skip it.
        if(len(PM25List)!=0):
                fp = open("./PM2.5_csv/"+arg_measurement+"/"+IDList[IDindex]+".csv", "w+")
                for PM25index in range(len(PM25List)): 
                        fp.write( str(PM25index)+","+str(PM25List[PM25index])+"\n");
                                                
                fp.close()




    

def main():

        #read in target measurement
		arg_measurement = sys.argv[1]
		if arg_measurement=='airbox':
			#if the folder already exsits , delete it and recreate it to avoid retainning outdated files.
			if os.path.exists("./PM2.5_csv/airbox"):
					shutil.rmtree('./PM2.5_csv/airbox')
					os.makedirs("./PM2.5_csv/airbox")

		if arg_measurement=='lass':
		#if the folder already exsits , delete it and recreate it to avoid retainning outdated files.
			if os.path.exists("./PM2.5_csv/lass"):
					shutil.rmtree('./PM2.5_csv/lass')
					os.makedirs("./PM2.5_csv/lass")



        #read in target past time if it exists in the cmd
		arg_pastTime=0
		if len(sys.argv)==3:
			arg_pastTime= sys.argv[2]

		

		getIDList(arg_measurement,IDList)
		for IDindex in range(len(IDList)):
				getPM25List(PM25List,arg_measurement,IDindex,IDList,arg_pastTime)
				write2file(arg_measurement,IDList,PM25List,IDindex)
				del PM25List[:]

		print('Measurement: ',arg_measurement)
		print('Total AirBox num: ',len(IDList))
		print('Response AirBox num: ',len(IDList)-lackDataID)
        
        
if __name__ == '__main__':
	main()

