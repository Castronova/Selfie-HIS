var map = L.map('map-preview').setView([51.505, -0.09], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	maxZoom: 18,
	id: 'mapbox.streets',
	accessToken: 'pk.eyJ1IjoiY2FzdHJvbmEiLCJhIjoiY2sxMjhxczE5MG95ZDNjb2k4dnFkbHB2ZSJ9.DX4vKS-D28BQgrjqTVxZgg'
}).addTo(map);


var locations = $.ajax({
    url:"?f=geojson",
          dataType: "json",
          success: function(responseJSON) {
	      var jsonLayer = L.geoJSON(responseJSON, {
		  onEachFeature: function (feature, layer) {
		      var text = ''
		      for (var k in feature.properties) {
			  text += '<b>'+k+'</b>: ';
			  text += feature.properties[k]+'</br>'
		      }
		      layer.bindPopup(text);
		  }}
	      ).addTo(map);
	      map.fitBounds(jsonLayer.getBounds());
	  },
          error: function (xhr) {
            alert(xhr.statusText)
	  }
});

//// create bbox shape that covers the extent of the provider's data
//var bbox_txt = document.getElementById('bbox').innerText;
//coords = bbox_txt.split(':')[1].trim().split(' ');
//var bbox_polygon = L.polygon([
//    [coords[0], coords[1]],
//    [coords[0], coords[3]],
//    [coords[2], coords[3]],
//    [coords[2], coords[1]]
//], {color:'red'});

//bbox_polygon.addTo(map);

// zoom to the extent of the bbox
//map.fitBounds(bbox_polygon.getBounds());

