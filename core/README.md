#Load all site ID
This program only need to execution one time unless the site ID be changed.
- Execution
	$ python lass_querySiteID.py
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
- Multiprocess will be updated soon.
- Load each site ID has been changed
    - All site IDs will be queried after executing lass_querySiteID.py.
    - lass_querySiteID.py will not going to create siteID.json, by contrast, it will return a dict that store the site data.
    - Have not test!!!
