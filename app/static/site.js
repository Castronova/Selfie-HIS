var map = L.map('map-preview').setView([51.505, -0.09], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
	maxZoom: 18,
	id: 'mapbox.streets',
	accessToken: 'pk.eyJ1IjoiY2FzdHJvbmEiLCJhIjoiY2sxMjhxczE5MG95ZDNjb2k4dnFkbHB2ZSJ9.DX4vKS-D28BQgrjqTVxZgg'
}).addTo(map);

// create bbox shape that covers the extent of the provider's data
var lat = parseFloat(document.getElementById('lat').innerText);
var lon = parseFloat(document.getElementById('lon').innerText);
var marker = L.marker([lat, lon]).addTo(map);

map.setView([lat, lon], 14);

