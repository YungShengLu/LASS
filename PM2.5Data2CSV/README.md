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

This program also print the measurement chosen by user to retrieve PM2.5 data ,total number of  AirBox device in that measurement , the number of  AirBox device that responds to "past time cmd: [H/D/W]" in that measurement,and the Device_id of the devices that doesn't have the requested data during the "past time " assined by user on terminal.

e.g.
```shell
Device_id: 28C2DDDD437C,no query result
Device_id: 28C2DDDD4423,no query result
Device_id: 28C2DDDD4528,no query result
Device_id: 28C2DDDD4572,no query result
Device_id: 28C2DDDD459D,no query result
('Measurement: ', 'airbox')
('Total AirBox num: ', 386)
('Response AirBox num: ', 381)
```

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