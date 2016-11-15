#!/usr/bin/python3
# target: "縣市"、"測站"、"風向"、"風速"、"陣風" 與 "時間"
"""
1. load html into string
2. parse string into class array
3. convert class into json

"""
import re
import json
import urllib.request
from datetime import datetime,timedelta   
#access influxDB and create database
from influxdb import InfluxDBClient
client = InfluxDBClient('localhost',8086,'root','root','LASS_WIND')
client.create_database('LASS_WIND')
#get today's year 
thisYear=str(datetime.now().date().year)



class Wind:
    def __init__(self, Direction=None, Speed=None, Gust=None, Time=None):
        self.Direction = Direction
        self.Speed = Speed
        self.Gust = Gust
        self.Time = Time
    def __str__(self):
        return '{{"Direction": "{0}", "Speed": "{1}", "Gust": "{2}", "Time": "{3}"}}'.format(self.Direction, self.Speed, self.Gust, self.Time)

class Observe:
    def __init__(self, County=None, Station=None, WindList=[]):
        self.County = County
        self.Station = Station
        self.WindList = WindList
    def __str__(self):
        WindListStr = "["
        for WindListIndex in range(0, len(self.WindList) - 1):
            WindListStr = "{0}{1}, ".format(WindListStr, self.WindList[WindListIndex])
        WindListStr = "{0}{1}".format(WindListStr, self.WindList[len(self.WindList) - 1])
        WindListStr = WindListStr + "]"
        return """{{
    "County": "{0}",
    "Station": "{1}",
    "WindList": {2}
}}""".format(self.County, self.Station, WindListStr)

### main
link = 'http://www.cwb.gov.tw/V7/observe/real/windAll.htm'

# with open('source.html', 'r') as f:
#     content_html = f.read()

with urllib.request.urlopen(link) as f:
    content_html = f.read().decode('UTF-8')

content_table = re.search(r"<table (.|\n|\r)*<\/table>", content_html).group(0)
content_tr_ary = re.findall(r"(<tr((((?!tr).)|\n|\r)*)<\/tr>)", content_table)

# get time_ary from content_tr_ary[0][0]
time_ary = []
content_tr_time = content_tr_ary[0][0]
content_time_ary = re.findall(r"(<th((((?!th).)|\n|\r)*)<\/th>)", content_tr_time)

for content_time_one in content_time_ary[2:-3]:
    time_ary.append( re.search(r"<th[^>]*>((((?!th).)|\n|\r)*)<\/th>", content_time_one[0]).group(1) )

# get observeList from content_tr_ary[2+][0]
observeList = [] # 


for content_tr_one in content_tr_ary[2:]:
    content_data_ary = re.findall(r"(<td((((?!td).)|\n|\r)*)<\/td>)", content_tr_one[0])
    len_content_data_ary = len(content_data_ary)
    
    observe = Observe()
    observe.County = re.search(r"<td[^>]*>((((?!td).)|\n|\r)*)<\/td>", content_data_ary[0][0]).group(1)
    observe.Station = re.search(r"<td[^>]*>((((?!td).)|\n|\r)*)<\/td>", content_data_ary[1][0]).group(1)
    
    wind = Wind()
    ## Direction, Speed, Gust
    time_ary_index = 0
    for index in range(2, len_content_data_ary - 3*3):
        if index % 3 == 2:
            result = re.search(r"title='([^']*)'", content_data_ary[index][0])
            if result == None:
                result = re.search(r"<td[^>]*>([^<]*)<\/td>", content_data_ary[index][0])
                # <td[^>]*>([^<]*)<\/td>
                # break
            wind.Direction = result.group(1)
        elif index % 3 == 0:
            result = re.search(r"<td[^>]*>(((?!td).)*)<\/td>", content_data_ary[index][0])
            if result == None:
                break
            wind.Speed = result.group(1)
        elif index % 3 == 1:
            result = re.search(r"<td[^>]*>(((?!td).)*)<\/td>", content_data_ary[index][0])
            if result == None:
                break
            wind.Gust = result.group(1)
            wind.Time = time_ary[time_ary_index]
            observe.WindList.append(wind)
            wind = Wind() # new a Wind object
            time_ary_index = time_ary_index + 1
    observeList.append(observe)

###store data into influxDB

for i in range(0,len(observeList)):
    
#    json_body=[{"measurement":"W2","tags":{"time":observeList[i].WindList[i].Time},"fields":{"County":observeList[i].County,"Station":observeList[i].Station,"Direction":observeList[i].WindList[i].Direction,"Speed":observeList[i].WindList[i].Speed,"Gust":observeList[i].WindList[i].Gust}}]
    
    #with year
    #json_body=[{"measurement":"wind","tags":{"Station":observeList[i].Station},"time":datetime.strptime(thisYear+'/'+observeList[i].WindList[i*24].Time,"%Y/%m/%d %H:%M" ),"fields":{"County":observeList[i].County,"Direction":observeList[i].WindList[i*24].Direction,"Speed":observeList[i].WindList[i*24].Speed,"Gust":observeList[i].WindList[i*24].Gust}}]
    
   
    #repair the date format of the parsed time data
    recordTime=thisYear+'/'+str(observeList[i].WindList[i*24].Time)
    #recordTime=observeList[i].WindList[i*24].Time
    recordTime=datetime.strptime(recordTime,"%Y/%m/%d %H:%M" )
    #recordTime=recordTime.replace(year = recordTime.year + 116)#since 1900
    #print (recordTime)
    #recordTime=datetime.strptime(str(recordTime),"%Y-%m-%d %H:%M:%S" )
    json_body=[{"measurement":"ancient_wind","tags":{"Station":observeList[i].Station},"timestamp":recordTime ,"fields":{"County":observeList[i].County,"Direction":observeList[i].WindList[i*24].Direction,"Speed":observeList[i].WindList[i*24].Speed,"Gust":observeList[i].WindList[i*24].Gust}}]
    
    client.write_points(json_body)

    
### print all data
#print('{')
#print('"result": [')
#for index in range(len(observeList)):
#     if index + 1 < len(observeList):
#         print('{0}'.format(observeList[index]), end=',\n')
#     else:
#         print('{0}'.format(observeList[index]))
#print(']}')
