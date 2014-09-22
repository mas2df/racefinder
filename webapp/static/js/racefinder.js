

var racefinder = {

    encoded_race_data: "",

    map: null,
    initial_lat: 39.0,
    initial_lon: -77.0,
    initial_zoom: 6,
    max_zoom: 18,

    init: function(encoded_race_data) {
        this.encoded_race_data = encoded_race_data;

        this.map = L.map('map').setView([this.initial_lat, this.initial_lon], this.initial_zoom);

        L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
            maxZoom: this.max_zoom,
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
                '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="http://mapbox.com">Mapbox</a>',
            id: 'mas2df.jgjm1j40'
        }).addTo(this.map);

        var markers = new L.MarkerClusterGroup();

        var race_list = this.decodeJSON(this.encoded_race_data);
        for (i in race_list) {
            var race = L.marker([race_list[i].location.lat, race_list[i].location.lon]);
            race.bindPopup("<ul><li>" + race_list[i].date + "<li>" + race_list[i].name + "<li>" + race_list[i].race_type + "<li><a href=\"" + race_list[i].race_site_url + "\" target=\"_blank\">link</a></ul>");
            markers.addLayer(race);
        }

        this.map.addLayer(markers);

    },

    decodeJSON: function (encodedJSON) {
        var decodedJSON = $('<div/>').html(encodedJSON).text();
        //TODO - figure out how to get rid of single quotes
        decodedJSON = decodedJSON.replace(/'/g, "")
        return $.parseJSON(decodedJSON);
    }
}