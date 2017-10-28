from events.gateways import PlacesGateway
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
                longitude=google_place['geometry']['location']['lng']
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
                longitude = google_place['geometry']['location']['lng']
            )
            location.save()
        else:
            location = location.first()

        return location

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
