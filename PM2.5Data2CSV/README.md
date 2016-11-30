#LASS influxDB PM2.5 data to CSV files




* Content: **DBData to csv**




* Version: **1**




* Update: **Nov 30, 2016 22:12**




​




##Framework




​




![Diagram](https://github.com/YungShengLu/LASS/blob/PM25_parser_fix/LASS_framework.png)




​




##Notice



##Description

###Retrieve PM2.5 data and store it as CSV file for each device in measurement 'airbox' / 'lass'.

This program retrieves PM2.5 data for each device stored in database:'PM25',measurement:'airbox'/'lass' of influxDB .
It sets up folders './PM2.5_csv/airbox' or './PM2.5_csv/airbox'(if these folder don't exist) according to your cmd to keep all the CSV files gernerated by this program that stores device's PM2.5 data of the requested measurement typed in cmd .
(The content of folders './PM2.5_csv/airbox' or './PM2.5_csv/airbox' will be updated every time user run the program to ensure all the CSV files are up-to-date.)


* **Format**
	```shell
	$ python DBData2csv.py [source] [past time]
		// [source] = [airbox / lass]
		// [past time]= [H/D/W] is "optional" ,it indicates the past time:1hr,24hrs,1 week respectively.
		If you ignore this arg , the program will set up csv files to store all the history PM2.5 data for each device.
	```

* **Example**
	```
	$ python DBData2csv.py airbox  
	//set up csv files to store all the history PM2.5 data for each device.

	$ python DBData2csv.py airbox H 
	//set up csv files to store the PM2.5 data of the past 1 hour for each device.


	$ python DBData2csv.py airbox D 
	//set up csv files to store the PM2.5 data of the past 24 hour for each device.

	$ python DBData2csv.py airbox W 
	//set up csv files to store the PM2.5 data of the past 1 week for each device.


	```