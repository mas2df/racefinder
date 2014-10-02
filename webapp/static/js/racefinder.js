

var racefinder = {

    encoded_race_data: "",
    race_list_json: null,
    race_distance_type_set: {},
    race_distance_set: {},
    race_type_set: {},

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

        this.race_list_json = this.decodeJSON(this.encoded_race_data);
        this.addRaceMarkerCluster();
        this.setRaceTypes();
        this.addRaceFilters();
    },

    addRaceMarkerCluster: function() {
        var markers = new L.MarkerClusterGroup();

        // Iterate over races
        for (i in this.race_list_json) {
            var race_json = this.race_list_json[i];

            // Create a marker for each race_marker
            var race_marker = L.marker([race_json.location.lat, race_json.location.lon]);
            race_marker.bindPopup("<ul><li>" + race_json.date + "<li>" + race_json.name + "<li>" + race_json.race_type + "<li><a href=\"" + race_json.race_site_url + "\" target=\"_blank\">link</a></ul>");
            markers.addLayer(race_marker);
        }

        this.map.addLayer(markers);
    },

    setRaceTypes: function() {
        
        // Iterate over races
        for (i in this.race_list_json) {
            var race_json = this.race_list_json[i];

            // Add the race_marker types to a set
//            var race_distance_type_list = race_json.race_distance_type;
//            for (j in race_distance_type_list) {
//                if (!(race_distance_type_list[j] in this.race_distance_type_set)) {
//                    this.race_distance_type_set[race_distance_type_list[j]] = true;
//                }
//            }

            var race_distance_list = race_json.race_distance;
            for (j in race_distance_list) {
                if (race_distance_list[j] && !(race_distance_list[j] in this.race_distance_set)) {
                    this.race_distance_set[race_distance_list[j]] = true;
                }
            }

            var race_type_list = race_json.race_type;
            for (j in race_type_list) {
                if (!(race_type_list[j] in this.race_type_set)) {
                    this.race_type_set[race_type_list[j]] = true;
                }
            }
        }
    },

    // Adds race types to the filters
    addRaceFilters: function() {
        var me = this;
        var ul = $("<ul>");

        var keys = Object.keys(this.race_distance_type_set);
        $.each(keys, function(i) {
            var input = $("<input>", {type: 'checkbox', value: keys[i], checked: "true"});
            input.on("click", {map: me.map}, me.applyFilter);
            var li = $("<li/>").append(input).append(keys[i]).appendTo(ul);
        });

        keys = Object.keys(this.race_type_set);
        $.each(keys, function(i) {
            var input = $("<input>", {type: 'checkbox', value: keys[i], checked: "true"});
            input.on("click", {map: me.map}, me.applyFilter);
            var li = $("<li/>").append(input).append(keys[i]).appendTo(ul);
        });

        keys = Object.keys(this.race_distance_set);
        $.each(keys, function(i) {
            var input = $("<input>", {type: 'checkbox', value: keys[i], checked: "true"});
            input.on("click", {map: me.map}, me.applyFilter);
            var li = $("<li/>").append(input).append(keys[i]).appendTo(ul);
        });

        $("#race-filter").append(ul);
    },

    applyFilter: function(event){
        var val = this.value;
        debugger;
        event.data.map.featureLayer.setFilter(function(f) {
            debugger;
            return f.properties['marker-symbol'] === 'fast-food';
        });
    },

    decodeJSON: function (encodedJSON) {
        var decodedJSON = $('<div/>').html(encodedJSON).text();
        //TODO - figure out how to get rid of single quotes
        decodedJSON = decodedJSON.replace(/'/g, "")
        return $.parseJSON(decodedJSON);
    }
}