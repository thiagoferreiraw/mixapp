from django.test import TestCase, RequestFactory
from events.services import PlacesGateway


class EventsGatewayTests(TestCase):

    def test_get_cities_by_description(self):
        gateway = PlacesGateway()
        response = gateway.get_cities_by_description("Guará", "en")

        self.assertEquals(response.status_code, 200)
        self.assertTrue(len(response.json()['predictions']) > 0)

    def test_get_places_by_id(self):
        gateway = PlacesGateway()
        response = gateway.get_places_by_id("ChIJN1t_tDeuEmsRUsoyG83frY4", "en")

        self.assertEquals(response.status_code, 200)
        self.assertTrue(len(response.json()['result']))

    def test_get_place_metadata_street_view_ok(self):
        gateway = PlacesGateway()
        response = gateway.get_place_metadata_street_view(-23.561414, -46.6580706)

        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.json()['status'], "OK")

    def test_get_place_metadata_street_view_invalid_place(self):
        gateway = PlacesGateway()
        response = gateway.get_place_metadata_street_view(0, 0)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['status'], "ZERO_RESULTS")
