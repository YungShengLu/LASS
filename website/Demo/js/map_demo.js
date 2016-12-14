var width = 900,
    height = 600,
    active = d3.select(null),
    centered;

//set the projection of the map
var projection = d3.geo.mercator()
    .center([120.979531, 23.995000])
    .scale(7000);

var path = d3.geo.path()
    .projection(projection)
    .pointRadius(0.5);

var svg = d3.select('.container-map')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

svg.append("rect")
    .attr('class', 'background')
    .attr('width', width)
    .attr('height', height)
    .on('click', zoom_reset);

var g = svg.append('g')
    .style('stroke-width', '0.5px');

var region = svg.append('g'),
    factory = svg.append('g'),
    airbox = svg.append('g'),
    lass = svg.append('g');

var tooltip = d3.select('.container-map')
    .append('div')
    .attr('class', 'hidden tooltip');

/* Draw layer of Taiwan */
d3.json('data/topojson/taiwan.json', function(error, taiwan) {
    if (error)
        return console.error(error);

    //display all regions.
    region.selectAll('path')
        .data(topojson.feature(taiwan, taiwan.objects.layer1).features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('class', 'region')
        .on('click', zoom_in)
        .on('mousemove', function(d) {
            var mouse = d3.mouse(svg.node()).map(function(d) {
                return parseInt(d);
            });
            tooltip.classed('hidden', false)
                .attr('style', 'left:' + (mouse[0] + 15) + 'px; top:' + (mouse[1] - 35) + 'px')
                .html(d.properties.COUNTYNAME);
        })
        .on('mouseout', function() {
            tooltip.classed('hidden', true);
        });

    region.append('path')
        .datum(topojson.mesh(taiwan, taiwan.objects.layer1, function(a, b) {
            return a !== b;
        }))
        .attr('d', path)
        .attr('class', 'mesh');
});

/* Draw layer of factory sites */
d3.json('data/topojson/factory_topo.json', function(error, site) {
    if (error)
        return console.error(error);

    //display all regions.
    factory.selectAll('path')
        .data(topojson.feature(site, site.objects.collection).features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('class', 'factory')
        .attr('id', function(d) {
            return d.properties.device_id;
        })
        .on('click', zoom_in)
        .on('mousemove', function(d) {
            var mouse = d3.mouse(svg.node()).map(function(d) {
                return parseInt(d);
            });
            tooltip.classed('hidden', false)
                .attr('style', 'left:' + (mouse[0] + 15) + 'px; top:' + (mouse[1] - 35) + 'px')
                .html(d.properties.device_id);
        })
        .on('mouseout', function() {
            tooltip.classed('hidden', true);
        });

    factory.append('path')
        .datum(topojson.mesh(site, site.objects.collection, function(a, b) {
            return a !== b;
        }))
        .attr('d', path)
        .attr('class', 'mesh');
});

/* Draw layer of AirBox sites */
d3.json('data/topojson/airbox_topo.json', function(error, site) {
    if (error)
        return console.error(error);

    //display all regions.
    airbox.selectAll('path')
        .data(topojson.feature(site, site.objects.collection).features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('class', 'airbox')
        .attr('id', function(d) {
            return d.properties.device_id;
        })
        .on('click', zoom_in)
        .on('mousemove', function(d) {
            var mouse = d3.mouse(svg.node()).map(function(d) {
                return parseInt(d);
            });
            tooltip.classed('hidden', false)
                .attr('style', 'left:' + (mouse[0] + 15) + 'px; top:' + (mouse[1] - 35) + 'px')
                .html(d.properties.device_id);
        })
        .on('mouseout', function() {
            tooltip.classed('hidden', true);
        });

    airbox.append('path')
        .datum(topojson.mesh(site, site.objects.collection, function(a, b) {
            return a !== b;
        }))
        .attr('d', path)
        .attr('class', 'mesh');
});

/* Draw layer of LASS sites */
d3.json('data/topojson/lass_topo.json', function(error, site) {
    if (error)
        return console.error(error);

    //display all regions.
    lass.selectAll('path')
        .data(topojson.feature(site, site.objects.collection).features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('class', 'lass')
        .attr('id', function(d) {
            return d.properties.device_id;
        })
        .on('click', zoom_in)
        .on('mousemove', function(d) {
            var mouse = d3.mouse(svg.node()).map(function(d) {
                return parseInt(d);
            });
            tooltip.classed('hidden', false)
                .attr('style', 'left:' + (mouse[0] + 15) + 'px; top:' + (mouse[1] - 35) + 'px')
                .html(d.properties.device_id);
        })
        .on('mouseout', function() {
            tooltip.classed('hidden', true);
        });

    lass.append('path')
        .datum(topojson.mesh(site, site.objects.collection, function(a, b) {
            return a !== b;
        }))
        .attr('d', path)
        .attr('class', 'mesh');
});

//click to zoom in
function zoom_in(d) {
    if (active.node() === this)
        return zoom_reset();

    active.classed('active', false);
    active = d3.select(this).classed('active', true);

    var bounds = path.bounds(d),
        dx = bounds[1][0] - bounds[0][0],
        dy = bounds[1][1] - bounds[0][1],
        x = (bounds[0][0] + bounds[1][0]) / 2,
        y = (bounds[0][1] + bounds[1][1]) / 2,
        scale = .9 / Math.max(dx / width, dy / height),
        translate = [width / 2 - scale * x, height / 2 - scale * y];

    console.log('scale: ' + scale + ' translate: ' + translate);

    region.transition()
        .duration(750)
        .style('stroke-width', 1.5 / scale + 'px')
        .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');

    factory.transition()
        .duration(750)
        .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');

    airbox.transition()
        .duration(750)
        .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');

    lass.transition()
        .duration(750)
        .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');

    document.getElementById('output_type').innerHTML = 'Type: ' + d.properties.type;
    document.getElementById('output_id').innerHTML = 'Device ID: ' + d.properties.id;
}

//click to reset zoom
function zoom_reset() {
    active.classed('active', false);
    active = d3.select(null);

    region.transition()
        .duration(750)
        .style('stroke-width', '1.1px')
        .attr('transform', '');

    factory.transition()
        .duration(750)
        .attr('transform', '');

    airbox.transition()
        .duration(750)
        .attr('transform', '');

    lass.transition()
        .duration(750)
        .attr('transform', '');


    document.getElementById('output_type').innerHTML = 'Type: ';
    document.getElementById('output_id').innerHTML = 'Device ID: ';
}


/*function test() {
    var type = document.getElementById('selectType').value,
        id = document.getElementById('inputID').value;

    document.getElementById('demo').innerHTML = 'Type: ' + type + ' ID: ' + id;
    console.log('Type: ' + type + ' ID: ' + id);
}*/

function search_zommIn() {
    var type = document.getElementById('selectType').value,
        id = document.getElementById('inputID').value;

    var d;

    if (type == 'factory') {
        active.classed('active', false);
        //active = d3.select(this).classed('active', true);
        factory.select('#' + id).classed('active', true);
        d = factory.select('#' + id);
        console.log(d)
    } else if (type == 'airbox') {
        active.classed('active', false);
        //active = d3.select(this).classed('active', true);
        airbox.select('#' + id).classed('active', true);
    } else if (type == 'lass') {
        active.classed('active', false);
        //active = d3.select(this).classed('active', true);
        lass.select('#' + id).classed('active', true);
    }

    var bounds = path.bounds(d);
    dx = bounds[1][0] - bounds[0][0],
        dy = bounds[1][1] - bounds[0][1],
        x = (bounds[0][0] + bounds[1][0]) / 2,
        y = (bounds[0][1] + bounds[1][1]) / 2,
        scale = .9 / Math.max(dx / width, dy / height),
        translate = [width / 2 - scale * x, height / 2 - scale * y];

    region.transition()
        .duration(750)
        .style('stroke-width', 1.5 / scale + 'px')
        .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');

    factory.transition()
        .duration(750)
        .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');

    airbox.transition()
        .duration(750)
        .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');

    lass.transition()
        .duration(750)
        .attr('transform', 'translate(' + translate + ')scale(' + scale + ')');

    //document.getElementById('output_type').innerHTML = d.properties.type;
    //document.getElementById('output_id').innerHTML = d.properties.id;
}
/* Show the specified layers */
/*function showLayer() {
    var layer = this;
    //var name = 
}*/
