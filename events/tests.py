from django.test import TestCase, RequestFactory
from mock import patch
from events.services import PlacesService, PlacesGateway
from events.models import User, City, Event, Category, Location
from datetime import datetime
from events.views.create_event_view import EventCreateView, EventCreateForm
import time


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
        self.assertTrue(City.objects.all())

    def test_get_and_save_location(self):
        service = PlacesService()
        location = service.get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        self.assertTrue(Location.objects.all())

class EventsFormsTests(TestCase):
    def test_insert_form_success(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        category = Category(description="Category", name="Cat")
        category.save()

        city = PlacesService().get_and_save_city("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        location = PlacesService().get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")

        form = EventCreateForm({
            'name': "Test Event",
            'description': "test Event",
            'duration': 1,
            'date': datetime.now(),
            'time': "15:00",
            'city': city.id,
            'location': "Location",
            'expected_costs': 200,
            'hosted_by': None,
            'location': location.id
        })

        self.assertTrue(form.is_valid())
        event = form.save(user_id=user.id)

        created_city = City.objects.filter(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4").first()

        self.assertEquals(event.name, "Test Event")
        self.assertEquals(event.description, "test Event")
        self.assertEquals(event.duration, 1)
        self.assertTrue(event.date is not None)
        self.assertTrue(event.time is not None)
        self.assertEquals(event.city.id, city.id)
        self.assertEquals(event.location.id, location.id )
        self.assertEquals(event.expected_costs, 200)
        self.assertEquals(event.hosted_by_id, user.id )

    def test_insert_form_fail(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        form = EventCreateForm({
            'description': "test Event",
            'duration': 1,
            'date_time': datetime.now(),
            'city': None,
            'location': "Location",
            'expected_costs': 200,
            'hosted_by': None,
            'category': []
        })

        self.assertFalse(form.is_valid())
        self.assertTrue("name" in form.errors)


class EventsViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('django.contrib.messages.success', return_value=True)
    def test_post_success(self, mock_messages):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        Event.objects.all().delete()

        request = self.factory.post("/events/new/", {
            "name": "Test",
            'description': "test Event",
            'duration': 1,
            'date': "2017-01-01",
            'time': "15:00",
            'location': "Location",
            'expected_costs': 200,
            'city': None,
            'location': None,
            'city_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
            'location_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4'
        })

        request.user = user

        response = EventCreateView().post(request)

        self.assertEquals(response.status_code, 302)

        event = Event.objects.all().first()

        self.assertEquals(event.description, "test Event")

        self.assertTrue(mock_messages.called)

