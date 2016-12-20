var map,
    sidebar,
    search;

/* Map arguments */
var position = [23.383, 120.583],
    scale = 8,
    minScale = 8,
    maxScale = 18;

var layer_airbox,
    layer_factory;

/* Legend arguments */
var legend,
    legendLabel = [],
    legendGrade = [0, 11, 23, 35, 41, 47, 53, 58, 64, 70],
    legendColor = ['#9CFF9C', '#31FF00', '#31CF00', '#FFFF00', '#FFCF00', '#FF9A00', '#FF6464', '#FF0000', '#990000', '#CE30FF']

/* Data cirlce arguments */
var datacircles = [],
    circle,
    dataAlpha = 0.5,
    dataRadius = 500,
    circleMaker,
    markerAlpha = 0.75,
    markerRadius = 1;

/* Define color square of legend. */
function getLegendColor(d) {
    return d < 11 ? legendColor[0] :
        d < 23 ? legendColor[1] :
        d < 35 ? legendColor[2] :
        d < 41 ? legendColor[3] :
        d < 47 ? legendColor[4] :
        d < 53 ? legendColor[5] :
        d < 58 ? legendColor[6] :
        d < 64 ? legendColor[7] :
        d < 70 ? legendColor[8] :
        legendColor[9];
}

/* Create legend. */
function createLegend() {
    legend = L.control({
        position: 'bottomright'
    });

    legend.onAdd = function(map) {
        var div = L.DomUtil.create('div', 'info legend');

        // Generate a label with a colored square for each interval.
        for (var i = 0; i < legendGrade.length; ++i) {
            div.innerHTML += legendLabel.push(
                '<i style="background:' + getLegendColor(legendGrade[i] + 1) + ';">&nbsp;&nbsp;&nbsp;&nbsp;</i> ' + legendGrade[i] + (legendGrade[i + 1] ? '&ndash;' + legendGrade[i + 1] : '+'));
        }
        div.innerHTML = legendLabel.join('<br>');

        return div;
    };
}

/* Create cirle on map. */
function createDataCircle() {
    for (i in data) {
    	var title = data[i].device_id;

        if (0 <= data[i].pollution && data[i].pollution < 11) {
            circle = L.circle([data[i].lat, data[i].lon], {
                color: legendColor[0],
                fillOpacity: dataAlpha,
                radius: dataRadius
            }).addTo(map);
            circleMaker = new L.CircleMarker([data[i].lat, data[i].lon], {
            	title: title,
                color: legendColor[0],
                fillOpacity: markerAlpha,
                radius: markerRadius
            });
        } else if (11 <= data[i].pollution && data[i].pollution < 21) {
            circle = L.circle([data[i].lat, data[i].lon], {
                color: legendColor[1],
                fillOpacity: dataAlpha,
                radius: dataRadius
            }).addTo(map);
            circleMaker = new L.CircleMarker([data[i].lat, data[i].lon], {
            	title: title,
                color: legendColor[1],
                fillOpacity: markerAlpha,
                radius: markerRadius
            });
        } else if (21 <= data[i].pollution && data[i].pollution < 31) {
            circle = L.circle([data[i].lat, data[i].lon], {
                color: legendColor[2],
                fillOpacity: dataAlpha,
                radius: dataRadius
            }).addTo(map);
            circleMaker = new L.CircleMarker([data[i].lat, data[i].lon], {
            	title: title,
                color: legendColor[2],
                fillOpacity: markerAlpha,
                radius: markerRadius
            });
        } else if (31 <= data[i].pollution && data[i].pollution < 41) {
            circle = L.circle([data[i].lat, data[i].lon], {
                color: legendColor[3],
                fillOpacity: dataAlpha,
                radius: dataRadius
            }).addTo(map);
            circleMaker = new L.CircleMarker([data[i].lat, data[i].lon], {
                title: title,
                color: legendColor[3],
                fillOpacity: markerAlpha,
                radius: markerRadius
            });
        } else if (41 <= data[i].pollution && data[i].pollution < 51) {
            circle = L.circle([data[i].lat, data[i].lon], {
                color: legendColor[4],
                fillOpacity: dataAlpha,
                radius: dataRadius
            }).addTo(map);
            circleMaker = new L.CircleMarker([data[i].lat, data[i].lon], {
                title: title,
                color: legendColor[4],
                fillOpacity: markerAlpha,
                radius: markerRadius
            });
        } else if (51 <= data[i].pollution && data[i].pollution < 61) {
            circle = L.circle([data[i].lat, data[i].lon], {
                color: legendColor[5],
                fillOpacity: dataAlpha,
                radius: dataRadius
            }).addTo(map);
            circleMaker = new L.CircleMarker([data[i].lat, data[i].lon], {
                title: title,
                color: legendColor[5],
                fillOpacity: markerAlpha,
                radius: markerRadius
            });
        } else if (61 <= data[i].pollution && data[i].pollution < 71) {
            circle = L.circle([data[i].lat, data[i].lon], {
                color: legendColor[6],
                fillOpacity: dataAlpha,
                radius: dataRadius
            }).addTo(map);
            circleMaker = new L.CircleMarker([data[i].lat, data[i].lon], {
                title: title,
                color: legendColor[6],
                fillOpacity: markerAlpha,
                radius: markerRadius
            });
        } else {
        	console.log(data[i].device_id);
            circle = L.circle([data[i].lat, data[i].lon], {
                color: legendColor[7],
                fillOpacity: dataAlpha,
                radius: dataRadius
            }).addTo(map);
            circleMaker = new L.CircleMarker([data[i].lat, data[i].lon], {
                title: title,
                color: legendColor[7],
                fillOpacity: markerAlpha,
                radius: markerRadius
            });
        }

        circle.bindPopup("SiteName: " + data[i].number + "<br /> Record timestamp : " + data[i].timestamp + "<br/> PM 2.5 : " + data[i].pollution + "<br /> ID: " + data[i].device_id);
        circleMaker.bindPopup("SiteName: " + data[i].number + "<br /> Record timestamp : " + data[i].timestamp + "<br/> PM 2.5 : " + data[i].pollution + "<br /> ID: " + data[i].device_id).openPopup();
        layer_airbox.addLayer(circleMaker);
    }
}

/* Initialize map */
function initMap() {
    // Load CSV file.
    d3.csv('data/csv/airbox.csv', function(error, d) {
        if (error) throw error;

        data = d;
        //window.alert('Catch ' + data.length + ' points')

        // Initializa the map.
        map = L.map('map').setView(position, scale);

        // Load the tile layers.
        map.addLayer(new L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            minZoom: minScale,
            maxZoom: maxScale,
            attribution: 'Map data &copy; OpenStreetMap contributors',
        }));

        layer_airbox = new L.LayerGroup();
        map.addLayer(layer_airbox);

        //Add search.
        search = new L.Control.Search({
            position: 'topright',
            layer: layer_airbox,
            initial: false,
            zoom: 12,
            marker: false
        });

        map.addControl(search);

        // Add sidebar.
        sidebar = L.control.sidebar('sidebar').addTo(map);

        // Add legend.
        createLegend();
        legend.addTo(map);

        // Add data in circle
        createDataCircle();
    });
}

/* Main function */
function init() {
    initMap();
}

/* Execute */
init();
