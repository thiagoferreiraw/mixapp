import requests
from django.conf import settings


class PlacesGateway:
    base_url = "https://maps.googleapis.com/"

    def get_cities_by_description(self, description, language):
        url = self.base_url + "maps/api/place/autocomplete/json"
        query = {
            'types': "(cities)",
            'input': description,
            'language': language,
            'key': settings.TOKEN_GOOGLE_PLACES_API
        }

        return requests.get(url, params=query)

    def get_places_by_id(self, place_id, language):
        url = self.base_url + "maps/api/place/details/json"
        query = {
            'placeid': place_id,
            'language': language,
            'key': settings.TOKEN_GOOGLE_PLACES_API
        }

        return requests.get(url, params=query)

    def get_place_metadata_street_view(self, lat, lng):
        url = self.base_url + "maps/api/streetview/metadata"
        query = {
            'location': "{},{}".format(lat, lng),
            'key': settings.TOKEN_GOOGLE_STREET_VIEW_API
        }

        return requests.get(url, params=query)
