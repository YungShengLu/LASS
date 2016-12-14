/*
 * D3 v3
 * OpenLayers v3.19.1
 */
/*
 *TODO:
 *  1. load map (OpenLayers or topojson)
 *  2. draw factories
 *  3. draw PM 2.5
 *  4. reset view
 *  5. layers control
 */
'use strict';
// ref. http://taqm.epa.gov.tw/taqm/tw/fpmi.htm
var pm25_colors = [
  {pm25: -1, color: '#FFFFFF'},
  {pm25:  0, color: '#9CFF9C'}, // rgb(156, 255, 156)
  {pm25: 12, color: '#31FF00'}, // rgb(49, 255, 0)
  {pm25: 24, color: '#31CF00'}, // rgb(49, 207, 0)
  {pm25: 36, color: '#FFFF00'}, // rgb(255, 255, 0)
  {pm25: 42, color: '#FFCF00'}, // rgb(255, 207, 0)
  {pm25: 48, color: '#FF9A00'}, // rgb(255, 154, 0)
  {pm25: 54, color: '#FF6464'}, // rgb(255, 100, 100)
  {pm25: 59, color: '#FF0000'}, // rgb(255, 0, 0)
  {pm25: 65, color: '#990000'}, // rgb(153, 0, 0)
  {pm25: 71, color: '#CE30FF'}  // rgb(206, 48, 255)
];
function getPm25Color(pm25) {
  for(var i = pm25_colors.length - 1; i >= 1; i--) {
    if(pm25 >= pm25_colors[i].pm25)
      return pm25_colors[i].color;
  }
  return pm25_colors[0].color;
}
function getPm25(data, device_id) {
  for(var i = 0; i < data.length; i++) {
    if(data[i].device_id == device_id) {
      return +data[i].pm25;
    }
  }
  return -1;
}

var map = new ol.Map({
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    })
  ],
  target: 'map',
  view: new ol.View({
    // https://www.openstreetmap.org/#map=7/23.583/120.583
    center: ol.proj.fromLonLat([120.583, 23.583]),
    zoom: 7
  })
});

// layer factories
(function() {
  var layer = new ol.layer.Vector({
    source: new ol.source.Vector({
      url: 'data/topojson/factory_topo.json',
      format: new ol.format.TopoJSON(),
      overlaps: true
    }),
    style: function(feature, resolution) {
      var style = new ol.style.Style({
        image: new ol.style.RegularShape({
          points: 5,
          radius: 6,
          stroke: new ol.style.Stroke({
            width: 2,
            color: 'black'
          }),
          fill: new ol.style.Fill({
            color: 'rgba(98,91,87,1.0)'
          })
        })
      });
      return [style];
    }
  });
  map.addLayer(layer);
})();

// layer PM25
(function() {
  var data = [];
  d3.text('data/csv/airbox.csv', function(text) {
    var rows = d3.csv.parseRows(text);
    for(var i = 0; i < rows.length; i++) {
      data.push({
        'type': 'lass',
        'device_id': rows[i][0],
        'pm25': rows[i][1],
        'time': rows[i][2]
      });
    }
  });
  var layer = new ol.layer.Vector({
    title: 'AirBox',
    source: new ol.source.Vector({
      url: 'data/topojson/airbox_topo.json',
      format: new ol.format.TopoJSON(),
      overlaps: true
    }),
    style: function(feature, resolution) {
      var fillColor = getPm25Color(getPm25(data, feature.get('device_id')));

      var style = new ol.style.Style({
        image: new ol.style.Circle({
          radius: 6,
          stroke: new ol.style.Stroke({
            width: 2,
            color: 'white'
          }),
          fill: new ol.style.Fill({
            //color: 'green'
            color: fillColor
          })
        })
      });
      return [style];
    }
  });
  map.addLayer(layer);
})();

(function() {
  var data = [];
  d3.text('data/csv/lass.csv', function(text) {
    var rows = d3.csv.parseRows(text);
    for(var i = 0; i < rows.length; i++) {
      data.push({
        'type': 'lass',
        'device_id': rows[i][0],
        'pm25': rows[i][1],
        'time': rows[i][2]
      });
    }
  });
  var layer = new ol.layer.Vector({
    title: 'LASS',
    source: new ol.source.Vector({
      url: 'data/topojson/lass_topo.json',
      format: new ol.format.TopoJSON(),
      overlaps: true
    }),
    style: function(feature, resolution) {
      var fillColor = getPm25Color(getPm25(data, feature.get('device_id')));

      var style = new ol.style.Style({
        image: new ol.style.Circle({
          radius: 6,
          stroke: new ol.style.Stroke({
            width: 2,
            color: 'white'
          }),
          fill: new ol.style.Fill({
            //color: 'blue'
            color: fillColor
          })
        })
      });
      return [style];
    }
  });
  map.addLayer(layer);
})();

