#LASS AirBox Parser
* Content: **airbox_parser**
* Version: **1.2**
* Update: **Nov 27, 2016 18:12**

##Framework

![Diagram](https://github.com/YungShengLu/LASS/blob/PM25_parser_fix/LASS_framework.png)

##Notice
* **History**
	* **Nov 15, 2016 23:51** - 無法抓到的超時測站ID，以及甚麼時候會故障(抓失敗的時間)
	* **Nov 27, 2016 18:12** - Update `parseSite` and delete the `querySite`.

* **Updates**
    * Parsing site number: **All data** from each source.
    * Delete the module `querySite`.
    * Database:
    	- `AirBox`: Store the data from the source *AirBox*.
    	- `LASS`: Store the data from the source *LASS*.
    	- `AirBox_record`: Store the record for parsing `AirBox` each time.
    	- `LASS_record`: Store the record for parsing `LASS` each time.
    * New parsing website:
    	- `AirBox`: http://nrl.iis.sinica.edu.tw/LASS/last-all-airbox.json
    	- `LASS`: http://nrl.iis.sinica.edu.tw/LASS/last-all-lass.json


##Description

###Parse the site data
This program is going to parse the specific city's site data.
* **Format**
	```shell
	$ python lass_parser.py [source]
		// [source] = [airbox / lass]
	```

* **Example**
	```
	$ python lass_parser.py airbox
	```
