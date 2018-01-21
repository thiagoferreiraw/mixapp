create_autocomplete_input = (function (input, options) {
    // store the original event binding function
    var _addEventListener = (input.addEventListener) ? input.addEventListener : input.attachEvent;

    function addEventListenerWrapper(type, listener) {
        // Simulate a 'down arrow' keypress on hitting 'return' when no pac suggestion is selected,
        // and then trigger the original listener.
        if (type == "keydown") {
            var orig_listener = listener;
            listener = function (event) {
                var suggestion_selected = $(".pac-item-selected").length > 0;
                if ((event.which == 13 || event.which == 9) && !suggestion_selected) {
                    var simulated_downarrow = $.Event("keydown", {
                        keyCode: 40,
                        which: 40
                    });
                    orig_listener.apply(input, [simulated_downarrow]);
                }

                orig_listener.apply(input, [event]);
            };
        }

        _addEventListener.apply(input, [type, listener]);
    }

    input.addEventListener = addEventListenerWrapper;
    input.attachEvent = addEventListenerWrapper;

    return new google.maps.places.Autocomplete(input, options);
});

mix_set_autocomplete_place_changed_event = (function(autocomplete,
                                                     place_id_input,
                                                     map,
                                                     marker,
                                                     zoom,
                                                     cascading_autocomplete_object,
                                                     cascading_autocomplete_id,
                                                     cascading_place_id,
                                                     lat_input_id,
                                                     lng_input_id,
                                                     cb){
    autocomplete.addListener('place_changed', function (e){
        var place = autocomplete.getPlace();
        if (!place.geometry) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            document.getElementById(place_id_input).value = ""
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }

        document.getElementById(place_id_input).value = place.place_id

        if (cb){
            cb()
        }

        if (map && zoom){
            map.setCenter(place.geometry.location);
            map.setZoom(zoom);
        }

        if (cascading_autocomplete_object && cascading_place_id){
            document.getElementById(cascading_place_id).value = "";
            document.getElementById(cascading_autocomplete_id).value = "";
            cascading_autocomplete_object.setBounds(place.geometry.viewport);
        }

        if (lat_input_id && lng_input_id){
            document.getElementById(lat_input_id).value = place.geometry.location.lat();
            document.getElementById(lng_input_id).value = place.geometry.location.lng();
        }

        if (marker){
            marker.setPosition(place.geometry.location);
        }

    });
});

mix_create_map = (function(element_id, lat, lng, zoom){
    return new google.maps.Map(document.getElementById('map'), {
        center: {lat: lat, lng: lng},
        zoom: zoom
    })
});

mix_create_map_marker = (function (map, lat, lng, title) {
    return new google.maps.Marker({
        position: {lat: lat, lng: lng},
        map: map,
        title: title
    });
});

