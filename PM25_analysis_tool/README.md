S#LASS Project

* Content: **In a target city, store each airbox's PM2.5 data as "csv" files **

* Version: **1.0**

* Update: **Nov 17, 2016 **


##Description



###Store each airbox's PM2.5 data as "csv" files in a target city typed in by user 

This program can get each airbox's PM2.5 data in a target city typed in by user ,and store it as a "csv" file for each airbox under a folder named the same name as the target city typed in by user with the first letter capitalized .
* **Execution Format**

        ```

        $ python airboxData2csv.py [city_name]

                // [city_name] = [taipei / newtaipei / taichung / tainan / kaohsiung]


        ```

* **Example**

        ```

        $ python airboxData2csv.py taipei

        ```

* **Output**

        Store all the PM2.5 data from each airbox in the city typed in by user as "csv" files 
        in a folder named Taipei,Newtaipei,Taichung,Tainan or Kaohsiung in this directory: "../timeFactorObservation". 
        
        The folder name depends on which city you typed in when executing this program .

