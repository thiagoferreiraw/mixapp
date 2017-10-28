from django.test import TestCase
from events.services import PlacesService


class EventsServiceTests(TestCase):

    def test_get_city_predictions(self):
        service = PlacesService()
        predictions = service.get_city_predictions("Guará", "en")

        self.assertTrue(predictions)

    def test_get_city_by_id(self):
        service = PlacesService()
        predictions = service.get_place_by_id("ChIJN1t_tDeuEmsRUsoyG83frY4", "en")

        self.assertTrue(predictions)

    def test_get_and_save_city(self):
        service = PlacesService()
        city = service.get_and_save_city("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        self.assertIsNotNone(city.description)

    def test_get_and_save_location(self):
        service = PlacesService()
        location = service.get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        self.assertIsNotNone(location.description)