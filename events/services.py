from events.gateways import PlacesGateway
from events.models import City


class PlacesService():
    def __init__(self):
        pass

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
                longitude = google_place['geometry']['location']['lng']
            )
            city.save()
        else:
            city = city.first()

        return city

