#Get Lateset PM2.5 data from influxDB and store it to CSV files,lass.csv and airbox.csv every 5 minutes




* Content: **Lateset PM2.5 data to csv**




* Version: **1**




* Update: **Dec 2, 2016 22:12**






##Notice



##Description

###Retrieve the latest PM2.5 data from measurement 'airbox' and 'lass' for each Device_ID and store it as CSV files every 5 minutes .

This program retrieves latest PM2.5 data for each device stored in database:'PM25',measurement:'airbox'and'lass' of influxDB .

Output is a CSV file that stores the latest PM2.5 data from measurement 'airbox' and 'lass' .

It stores output CSV file in '/var/www/html/Demo/csv/' directory. 

###The output :
	'airbox.csv' and 'lass.csv' ,and store these files in '/var/www/html/Demo/csv/' directory


###The format of output :
###"'Device_id','Latest PM2.5','time'"
e.g.
```shell

	801F02000010,11,2016-12-02T14:20:01Z
	74DA38A86962,20,2016-12-02T14:20:01Z
	74DA38A86960,18,2016-12-02T14:20:01Z
	74DA38A8695E,21,2016-12-02T14:20:01Z
	74DA38A8695C,21,2016-12-02T14:20:01Z
	74DA38A86958,27,2016-12-02T14:20:01Z
```




This program also print the measurement chosen by user to retrieve PM2.5 data ,and total number of  AirBox device in that measurement .


e.g.
```shell
('Measurement: ', 'airbox')
('Total AirBox num: ', 386)
```





* **Execution Format**
	```shell
	$ python GetLatestPM25.py [source] 
		// [source] = [airbox / lass]
		

* **Example**
	```
	$ python GetLatestPM25.py airbox  
	//set up airbox.csv to store latest PM2.5 data for each device.

	```