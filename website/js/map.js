'use strict';
var position = [23.583, 120.583],
    minZoom =  7,
    defaultZoom = 8,
    maxZoom = 18,
    aqiColor = ['#9CFF9C', '#31FF00', '#31CF00', '#FFFF00', '#FFCF00',
    '#FF9A00', '#FF6464', '#FF0000', '#990000', '#CE30FF'];
var map;

function getAqiColor(aqi) {
    return aqi < 11 ? aqiColor[0] :
        aqi < 23 ? aqiColor[1] :
        aqi < 35 ? aqiColor[2] :
        aqi < 41 ? aqiColor[3] :
        aqi < 47 ? aqiColor[4] :
        aqi < 53 ? aqiColor[5] :
        aqi < 58 ? aqiColor[6] :
        aqi < 64 ? aqiColor[7] :
        aqi < 70 ? aqiColor[8] :
        aqiColor[9];
}

function renderAirData(data) {
    var opacity = 0.5,
        radius = 500;
    var title,
        color,
        circle,
        strPopup;

    var I = data.length;
    for(var i = 0; i < I; i++) {
        title = data[i].device_id;
        color = getAqiColor(data[i].pollution);

        circle = L.circle([data[i].lat, data[i].lon], {
            color: color,
            fillColor: color,
            fillOpacity: opacity,
            radius: radius
        }).addTo(map);

        strPopup = "SiteName: " + (i + 1).toString()
            + "<br /> Record timestamp : " + data[i].timestamp
            + "<br/> PM 2.5 : " + data[i].pollution
            + "<br /> ID: " + data[i].device_id;
        circle.bindPopup(strPopup);
    }
}

// init map
(function() {
    var airData = [];

    map = L.map('map').setView(position, defaultZoom);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            minZoom: minZoom,
            maxZoom: maxZoom,
            continuousWorld: false,
            attribution: 'Map data &copy; OpenStreetMap contributors'
            }).addTo(map);

    // load csv
    d3.csv('data/csv/lass.csv', function(error, data) {
        if(error) throw error;
        airData = airData.concat(data);
    });
    d3.csv('data/csv/airbox.csv', function(error, data) {
        if(error) throw error;
        airData = airData.concat(data);

        console.log('Number of data: ' + airData.length);
        // callback renderAirData
        renderAirData(airData);
    });

    // add sidebar
    L.control.sidebar('sidebar').addTo(map);
})();

