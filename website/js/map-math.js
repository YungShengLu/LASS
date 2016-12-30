var D2R   = +(Math.PI / 180.0);
var cos18 = +Math.cos(18 * D2R),
    sin18 = +Math.sin(18 * D2R),
    cos36 = +Math.cos(36 * D2R),
    sin36 = +Math.sin(36 * D2R);
var ratioPentagon = [
  L.latLng( (Math.sqrt(5)-1)/4,  Math.sqrt(10+2*Math.sqrt(5))/4),
  L.latLng(     1,      0),
  L.latLng( (Math.sqrt(5)-1)/4, -Math.sqrt(10+2*Math.sqrt(5))/4),
  L.latLng(-(Math.sqrt(5)+1)/4, -Math.sqrt(10-2*Math.sqrt(5))/4),
  L.latLng(-(Math.sqrt(5)+1)/4,  Math.sqrt(10-2*Math.sqrt(5))/4)
];
var point2PentagonArray = function(p, r) {
  var result = [];
  var i;
  for(i = 0; i < 5; ++i) {
    result.push(L.latLng((p.lat + ratioPentagon[i].lat * r),
          (p.lng + ratioPentagon[i].lng * r)));
  }
  return result;
};

