from events.gateways import PlacesGateway, settings
from events.models import City, Location


class PlacesService:

    def get_city_predictions(self, description, language):
        response = PlacesGateway().get_cities_by_description(description, language)
        return response.json()['predictions']

    def get_place_by_id(self, place_id, language):
        response = PlacesGateway().get_places_by_id(place_id, language)
        return response.json()['result']

    def get_and_save_city(self, place_id, language):
        city = City.objects.filter(place_id=place_id)
        if len(city) == 0:
            google_place = self.get_place_by_id(place_id, language)
            city = City(
                place_id=google_place['place_id'],
                description=google_place['formatted_address'],
                latitude=google_place['geometry']['location']['lat'],
                longitude=google_place['geometry']['location']['lng'],
                timezone=google_place['utc_offset'] / 60,
            )
            city.save()
        else:
            city = city.first()

        return city

    def get_and_save_location(self, place_id, language):
        location = Location.objects.filter(place_id=place_id)
        if len(location) == 0:
            google_place = self.get_place_by_id(place_id, language)
            location = Location(
                place_id=google_place['place_id'],
                description=google_place['formatted_address'],
                latitude=google_place['geometry']['location']['lat'],
                longitude=google_place['geometry']['location']['lng'],
                timezone=google_place['utc_offset'] / 60,
            )

            location.save()
        else:
            location = location.first()

        return location

    def get_images_street_view(self, lat, lng):
        images = []

        status_api = PlacesGateway().get_place_metadata_street_view(lat, lng).json()

        if status_api['status'] != 'OK':
            return images

        for heading in [0, 60, 120, 180, 240, 300, 360]:
            token = settings.TOKEN_GOOGLE_STREET_VIEW_API
            size = "640x360"
            coordinates = "{},{}".format(lat, lng)
            images.append("https://maps.googleapis.com/maps/api/streetview?size={}&location={}&heading={}&key={}".format(size,
                                                                                                                 coordinates,
                                                                                                                 heading,
                                                                                                                 token))
        return images

    def get_images_google_place(self, place_id, language):
        images = []
        google_place = self.get_place_by_id(place_id, language)
        if "photos" in google_place:
            for photo in google_place['photos']:
                images.append(
                    "https://maps.googleapis.com/maps/api/place/photo?maxheight={}&photoreference={}&key={}"
                    .format(1000, photo['photo_reference'], settings.TOKEN_GOOGLE_PLACES_API))

        return images

    def get_city_for_request(self, request):
        if not (request.POST['city_place_id'] is None or request.POST['city_place_id'] == ""):
            city = self.get_and_save_city(request.POST['city_place_id'], "en")
            request.POST._mutable = True
            request.POST['city'] = city.id
        return request

    def get_location_for_request(self, request):
        if request.POST['location_place_id'] is not None and request.POST['location_place_id'] != "":
            location = self.get_and_save_location(request.POST['location_place_id'], "en")
            request.POST._mutable = True
            request.POST['location'] = location.id
        return request