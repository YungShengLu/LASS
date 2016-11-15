LASS Project
content: core
version: 1.1
update: Nov 15, 2016 - 23:51

===

#Query all site ID

This program only need to execution one time unless the site ID be changed.
- Execution
	$ python lass_querySiteID.py -q
- Output
	return a dict that store all city's site IDs    


#Parse the site data

This program is going to parse the specific city's site data.
- Format
	$ python lass_parser.py [city_name]
	// [city_name] = [taipei / newtaipei / taichung / tainan / kaohsiung]
- Example
	$ python lass_parser.py tainan
- Structure
    - Use the input dict of the specific city's site IDs to parse the site data.
    - The most biggest issue is that we have to parse each site data by query the site ID.
        - Waste too much time to parse.
        - Can be solved by parsing a one of website that store all site data under the specific city "if possible".
        - Most Probably solution: multiprocesses programming
            - Divided the specific city's site into several part.
            - Multithreads and multiprocesses

#Notice

- This version has changed the followings:
    - Parsing site number: 12
    - Turn off the "sleep time"
    - Use the "requests" module for requiring LASS web data.
    - Set up the request timeout for 25 seconds.
- TODO:
    - Parallel version will be updated soon.
