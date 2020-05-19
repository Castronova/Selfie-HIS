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

// create bbox shape that covers the extent of the provider's data
var lat = parseFloat(document.getElementById('lat').innerText);
var lon = parseFloat(document.getElementById('lon').innerText);
//var marker = L.marker([lat, lon]).addTo(map);

//map.setView([lat, lon], 14);

