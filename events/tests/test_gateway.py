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
