var map = L.map('map-preview').setView([51.505, -0.09], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        maxZoom: 18,
        id: 'outdoors-v11',
        accessToken: 'pk.eyJ1IjoiY2FzdHJvbmEiLCJhIjoiY2sxMjhxczE5MG95ZDNjb2k4dnFkbHB2ZSJ9.DX4vKS-D28BQgrjqTVxZgg'
}).addTo(map);


var locations = $.ajax({
    url:"?f=geojson",
          dataType: "json",
          success: function(responseJSON) {
              var markers = L.markerClusterGroup();
              var jsonLayer = L.geoJSON(responseJSON, {
                  onEachFeature: function (feature, layer) {
                      var text = ''
                      for (var k in feature.properties) {
                          text += '<b>'+k+'</b>: ';
                          text += feature.properties[k]+'</br>'
                      }
                      layer.bindPopup(text);
                  }}
              )
              markers.addLayer(jsonLayer);
              map.addLayer(markers);
              map.fitBounds(jsonLayer.getBounds());
          },
          error: function (xhr) {
            alert(xhr.statusText)
          }
});
