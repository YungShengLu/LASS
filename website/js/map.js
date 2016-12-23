'use strict';
var position = [23.583, 120.583],
    minZoom =  7,
    defaultZoom = 8,
    maxZoom = 18,
    legendGrade = [0, 11, 23, 35, 41, 47, 53, 58, 64, 70],
    legendColor = ['#9CFF9C', '#31FF00', '#31CF00', '#FFFF00', '#FFCF00',
    '#FF9A00', '#FF6464', '#FF0000', '#990000', '#CE30FF'],
    factoryColor = '#888888';
var map,
    sidebar,
    layerAirData;

function getLegendColor(aqi) {
    return aqi < 11 ? legendColor[0] :
        aqi < 23 ? legendColor[1] :
        aqi < 35 ? legendColor[2] :
        aqi < 41 ? legendColor[3] :
        aqi < 47 ? legendColor[4] :
        aqi < 53 ? legendColor[5] :
        aqi < 58 ? legendColor[6] :
        aqi < 64 ? legendColor[7] :
        aqi < 70 ? legendColor[8] :
        legendColor[9];
}

function renderAirData(data) {
    var opacity = 0.5,
        radiusCircle = 500,
        radiusCircleMarker = 1;
    var title,
        color,
        circle,
        circleMarker,
        strPopup;

    var I = data.length;
    for (var i = 0; i < I; i++) {
        title = data[i].device_id;
        color = getLegendColor(data[i].pollution);

        circle = L.circle([data[i].lat, data[i].lon], {
            color: color,
            fillColor: color,
            fillOpacity: opacity,
            radius: radiusCircle
        }).addTo(map);
        circleMarker = new L.CircleMarker([data[i].lat, data[i].lon], {
            title: data[i].device_id,
            color: color,
            fillOpacity: opacity,
            radius: radiusCircleMarker
        });

        strPopup = "SiteName: " + (i + 1).toString()
            + "<br /> Record timestamp : " + data[i].timestamp
            + "<br/> PM 2.5 : " + data[i].pollution
            + "<br /> ID: " + data[i].device_id;
        circle.bindPopup(strPopup);
        circleMarker.bindPopup(strPopup);
        layerAirData.addLayer(circleMarker);
    }
}

function createLegend() {
    var legendLabel = [];

    var legend = L.control({
        position: 'bottomright'
    });
    legend.onAdd = function(map) {
        var div = L.DomUtil.create('div', 'info legend');

        div.innerHTML = '<i style="background: ' + factoryColor
            + ';">&nbsp;&nbsp;&nbsp;&nbsp;</i> factory<br/>';

        // Generate a label with a colored square for each interval.
        for (var i = 0; i < legendGrade.length; ++i) {
            legendLabel.push('<i style="background:'
                    + getLegendColor(legendGrade[i] + 1)
                    + ';">&nbsp;&nbsp;&nbsp;&nbsp;</i> '
                    + legendGrade[i]
                    + (legendGrade[i + 1] ? '&ndash;'+legendGrade[i + 1] : '+')
                    );
        }
        div.innerHTML += legendLabel.join('<br>');

        return div;
    };
    return legend;
}

// init map
function initMap() {
    var airData = [],
        search;

    map = L.map('map').setView(position, defaultZoom);
    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            minZoom: minZoom,
            maxZoom: maxZoom,
            continuousWorld: false,
            attribution: 'Map data &copy; OpenStreetMap contributors'
            }).addTo(map);

    layerAirData = new L.LayerGroup();
    map.addLayer(layerAirData);

    // load factories
    d3.csv('data/csv/factories.csv', function(error, data) {
        if(error) throw error;
        var color = factoryColor;
        var circle,
            strPopup;

        var I = data.length;
        for(var i = 0; i < I; i++) {
            circle = L.circle([data[i].latitude, data[i].longitude], {
                color: color,
                fillColor: color,
                fillOpacity: 0.5,
                radius: 500
            }).addTo(map);

            strPopup = "ID: " + data[i].id
                + "<br/> FactoryName: " + data[i].name
                + "<br/> Type: " + data[i].type;
            circle.bindPopup(strPopup);
        }
    });

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
    sidebar = L.control.sidebar('sidebar').addTo(map);

    // add legend
    createLegend().addTo(map);

    // add search
    search = new L.Control.Search({
        position: 'topright',
        layer: layerAirData,
        initial: false,
        zoom: 12,
        marker: false
    });
    map.addControl(search);
}

window.onload = initMap;

