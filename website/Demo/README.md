LASS Demo website

===

##Installation

* **Step 1. Git clone**
	```
	$ git clone git@github.com:
	```

* **Step 2. Setup HTTP server**
	* Open the terminal.
	* Change directory to the folder of this demo.
		```
		$ cd ../demo
		```

	* Using Python to setup ```SimpleHTTPServer```
		```
		$ python -m SimpleHTTPServer
		```

* **Step 3. Open browser**
	* Connect to the ```localhost```.
		```
		0.0.0.0:8000/demo.html
		```
	


##Notice

* This demo is using ```topojson``` to represent the map.
	* The file is under the following directory: ```../demo/topojson/taiwan.json```.
	* If you only have other format of geograhic data, i.e, **KML**, **GeoJson**... etc, there are some useful tools for you to convert the file.
		* **KML** to **GeoJson**: http://mapbox.github.io/togeojson/
		* **GeoJson** to **TopoJson**: http://jeffpaine.github.io/geojson-topojson/


* Some useful examples for d3.js to represent map
	* Let’s Make a Map: http://bost.ocks.org/mike/map/
	* Map Pan & Zoom I: http://bl.ocks.org/mbostock/8fadc5ac9c2a9e7c5ba2
	* Map Pan & Zoom II: http://bl.ocks.org/mbostock/eec4a6cda2f573574a11
	* click-to-zoom via transform: http://bl.ocks.org/mbostock/2206590

