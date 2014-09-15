function decodeJSON(encodedJSON) {
    var decodedJSON = $('<div/>').html(encodedJSON).text();
    //TODO - figure out how to get rid of single quotes
    decodedJSON = decodedJSON.replace(/'/g, "")
    return $.parseJSON(decodedJSON);
}

var map = L.map('map').setView([39.0, -77.0], 6);

L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
    id: 'mas2df.jgjm1j40'
}).addTo(map);

var encoded_races = "{{ races }}";
var race_list = decodeJSON(encoded_races);
for (i in race_list) {
    L.marker([race_list[i].location.lat, race_list[i].location.lon]).addTo(map)
}
