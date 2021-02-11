#!/usr/bin/python3

_msg_monitors = """
air monitors in Tainan City: (id)
				airbox
								74DA38AF489E
								74DA38AF487A
								74DA38AF4842
								74DA38AF482E
								74DA38AF4812
								74DA38AF479A
								74DA3895E068
								74DA3895E04C
								74DA3895DFF6
								74DA3895C39E
								74DA388FF4F8
								28C2DDDD479F
								28C2DDDD479C
								28C2DDDD415F
				lass
								YK_160
								FT1_CCH01
"""



from influxdb import InfluxDBClient

#from prefixspan import frequent_rec,topk_rec


import sys
from collections import defaultdict
from heapq import heappop, heappush
import operator
#from consequentPattern import pattern_mining,genCandidate
import consequentPattern
import HillFunction

db=[]

def query_interval_by_device_id(client, measurement='', device_id='', late_time='now()', duration='1h'):
				# return type: Raw JSON from InfluxDB
				#print(late_time)
				early_time = late_time + ' - '  + duration
				#print(early_time)
				str_query = 'select "PM2.5" from ' + measurement + ' where "Device_id" = \'' + device_id + '\' and time <= ' + late_time + ' and time > ' + early_time
				return client.query(str_query).raw

def get_pm25s_from_query(json={}):
				# return type: list
				ret = []
				for value in json['series'][0]['values']:
								#print(value[1])
								ret.append(value[1])
				return ret

def pm25_to_pattern(pm25=0):
				# return type: str
				_pm25_levels = [11, 23, 35, 41, 47, 53, 58, 64, 70]
				_patterns =    ['a','b','c','d','e','f','g','h','i','j']
				for i in range(0, len(_pm25_levels)):
								
								if pm25 <= _pm25_levels[i] :
												return _patterns[i]+' '
								elif pm25>_pm25_levels[len(_pm25_levels)-1]:
												return _patterns[len(_patterns)-1]+' '

				return _patterns[len(_pm25_levels)]

def pm25s_to_patterns(pm25s=[]):
				# return type: list
				ret = []
				for pm25 in pm25s:
								ret.append(pm25_to_pattern(pm25))
				return ret


def predictPM25Level(predictionRef=[]):
				predictionCandidateDic={}
				for(freq,patt) in predictionRef:
								if( patt[len(patt)-1] not in predictionCandidateDic ):
												predictionCandidateDic[patt[len(patt)-1]] = 0
								predictionCandidateDic[patt[len(patt)-1]]=predictionCandidateDic[patt[len(patt)-1]]+freq
				print("predictionCandidateDic : {}".format(predictionCandidateDic))

				maxFreq=0
				predictionResult=' '
				for  pattRef,freqRef in predictionCandidateDic.iteritems():
				
								if(freqRef>maxFreq):
												maxFreq=freqRef
												predictionResult=pattRef

				return predictionResult




if __name__=='__main__':
				#init predict pivot
				predictPivot=0
				
			
				client = InfluxDBClient(host='127.0.0.1', port=8086, database='PM25')
				#prefixSpanCmd=raw_input( 'Please enter (frequent | top-k) <threshold>').split()

				#get PM2.5 data from the selected airbox device
				print(_msg_monitors)
				measurement, device_id = raw_input('Input measurement and id: (seperated by space) ').split()
				print('measurement = {0}, device_id = {1}'.format(measurement, device_id))
				print('') # new line
				for h in range(0,24):#past 1 to 24 hour
								try:
												result = query_interval_by_device_id(client, measurement, device_id, 'now() - ' + str(h) + 'h' ,'1h')
												
												patternList=(''.join(pm25s_to_patterns(get_pm25s_from_query(result)))).split()
												
												if(h==0):
																predictPivot=patternList[len(patternList)-1]
																
												
												db.append(patternList)
				


							
				
												



								except:
												print('[debug] There may be no result in this query.')
												print('[debug]   measurement = {0}, device_id = {1}, h = {2}'.format(measurement, device_id,h))



				#argv = docopt(__doc__)

				# db = [
								# [int(v) for v in line.rstrip().split(' ')]
								# for line in sys.stdin
				# ]
				'''
				db = [
								[0, 1, 2, 3, 4],
								[1, 1, 1, 3, 4],
								[2, 1, 2, 2, 0],
								[1, 1, 1, 2, 2],
				]
				'''
							
				'''
				db = [
								['a',('a','b','c'),('a','c'),'d',('c','f')],
								[('a','d'),'c',('b','c'),('a','e')],
								[('e','f'),('a','b'),('d','f'),'c','b'],
								['e','g',('a','f'),'c','b','c'],
				]
				'''

				formatDB=[]
				tempStr=""
				k=len(db)

				for i in range(0,len(db)):
								print(" ")
								print ("PM2.5 level in the {}th hour in the past".format(k))
								print (db[k-1])
								k=k-1
								tempStr = ''.join(db[k])

								formatDB.append(tempStr)
								tempStr=""
				
				

				

				element = [['a', 1], 
															['b', 1],
															['c', 1],
															['d', 1],
															['e', 1], 
															['f', 1], 
															['g', 1], 
															['h', 1],
															['i', 1],
															['j', 1]
												]
												#minimum support=2
				min_support = 2
				patternLenDict = consequentPattern.pattern_mining(formatDB, element, min_support)
				del patternLenDict[1] # remove  entry with key 'Length ==1' becuase it's meaningless for sequential pattern mining app
				del patternLenDict[13]# remove  entry with key 'Length ==1' becuase it's meaningless for sequential pattern mining app
				print(patternLenDict)
				print (formatDB)
				dataset_weight_applied=HillFunction.MultiplyHillFunWeight(patternLenDict)
				#print ("dataset with weight applied={0}".format(dataset_weight_applied))
				
				#sort the freq of each pattern after weight applied.
				sorted_dataset={}
				lenCount=2
				for pattern_len, pattern_collectionDict in dataset_weight_applied.iteritems():	
					for pattern, freq in pattern_collectionDict.iteritems():			
						sorted_set = sorted(dataset_weight_applied[pattern_len].items(), key=operator.itemgetter(1))
						sorted_set.reverse()
					sorted_dataset[lenCount]=sorted_set
					lenCount=lenCount+1

				print ("After sorting= {0}".format(sorted_dataset))

				print (" ")#/n


				
				#get referech string from the most recent 12 PM2.5 data of the device.
				lenFormatDB=len(formatDB)
				referenceString=formatDB[lenFormatDB-1]
				i=2
				while len(referenceString)<12:
						referenceString=formatDB[lenFormatDB-i]+referenceString
						
						i=i+1
				
				print(referenceString)


				#compare the most matched pattern of each length
				candidatePredictionPattDict={}
				cur_len=2
				for pattern_len, pattern_collectionDict in sorted_dataset.iteritems():	
					for i in range(0,len(sorted_dataset[pattern_len])):
						#print(sorted_dataset[pattern_len][i])
						print("foundPatt    ={0}".format(sorted_dataset[pattern_len][i][0]))

						comparedString=""
						for j in range(0,cur_len-1):
							comparedString+=sorted_dataset[pattern_len][i][0][j]
						print("comparedPatt ={0}".format(comparedString))
						print("referencePatt={0}".format(referenceString[-len(comparedString):]))
						
						if(comparedString==referenceString[-len(comparedString):]):
							print("~~~~Pattern matched!!~~~~~")
							candidatePredictionPattDict[sorted_dataset[pattern_len][i][0]]=sorted_dataset[pattern_len][i][1]
						print("")#\n
					cur_len=cur_len+1
				
				#sort the candidatePredictionPatt
				sorted_candidatePredictionPattDict = sorted(candidatePredictionPattDict.items(), key=operator.itemgetter(1))
				sorted_candidatePredictionPattDict.reverse()
				print("candidatePredictionPatts of Device :{0}  is  {1}".format(device_id,sorted_candidatePredictionPattDict))
				#print ("The prediction PM2.5 level in the next 5 mins is : {}".format(predictLevel))

				#check if the candidatePredictionPattDict is empty or not.
				'''
				if(bool(candidatePredictionPattDict) ):
				'''













				'''
				#to keep prediction reference
				predictionRef=[]
				#print out GSP result

				print ("The last datum is : {}".format(predictPivot))
				for (freq, patt) in results:
								#print out only the patterns that have 2<=length<=6,
								#have the latest data involved .        
							
								if( len(patt)>=2 and len(patt)<=6 and  predictPivot in patt ):
												if(patt.count(predictPivot)>1 or patt[len(patt)-1]!=predictPivot):
																print("{}: {}".format(patt, freq))

																#add reference for prediction to a list
																predictionRef.append((freq, patt))



				#predict PM2.5 level in the next 5 mins
				predictLevel=predictPM25Level(predictionRef)
				print ("The prediction PM2.5 level in the next 5 mins is : {}".format(predictLevel))
				'''








			

			