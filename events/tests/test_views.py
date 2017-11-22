from django.test import TestCase, RequestFactory
from mock import patch
from events.models import User, City, Event, Category, Location
from datetime import datetime, timedelta
from events.views.create_event_view import EventCreateView
from events.views.event_details_view import EventDetailsView
from events.views.search_event_view import EventSearchView


class EventsViewsTests(TestCase):
    fixtures = ['categories.json', 'languages.json', "test_data.json"]

    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        self.client.login(username="tester", password="top_secret")

    def test_get_create_success(self):
        response = self.client.get("/events/new/")
        self.assertEquals(response.status_code, 200)

    @patch('django.contrib.messages.success', return_value=True)
    def test_post_create_success(self, mock_messages):
        response = self.client.post("/events/new/", {
            'name': "Test Event",
            'description': "test Event",
            'duration': 1,
            'date': (datetime.now() + timedelta(days=1)).date(),
            'time': datetime.now().time(),
            'expected_costs': 200,
            'hosted_by': self.user.id,
            "location_lat": "-33.8688",
            "location_lng": "151.2195",
            'category': Category.objects.get(pk=1).id,
            'city_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
            'location_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
            'foreign_language': 1,
            'native_language': 2,
        })

        self.assertEquals(response.status_code, 302)

        event = Event.objects.all().order_by('-id').first()

        self.assertEqual(response.url, "/events/edit/{}/image/".format(event.id))

        self.assertEquals(event.description, "test Event")

        self.assertTrue(mock_messages.called)

        city = City.objects.filter(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4").first()

        self.assertIsNotNone(city.description)

        location = Location.objects.filter(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4").first()

        self.assertIsNotNone(location.description)


class EventDetailsViewsTests(TestCase):
    fixtures = ['categories.json', 'languages.json']

    def setUp(self):
        self.factory = RequestFactory()

    @patch('django.contrib.messages.success', return_value=True)
    def test_get_success(self, mock_messages):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        Event.objects.all().delete()

        request = self.factory.post("/events/new/", {
            'name': "Test Event",
            'description': "test Event",
            'duration': 1,
            'date': (datetime.now() + timedelta(days=1)).date(),
            'time': datetime.now().time(),
            'expected_costs': 200,
            'hosted_by': user.id,
            "location_lat": "-33.8688",
            "location_lng": "151.2195",
            'category': Category.objects.get(pk=1).id,
            'city_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
            'location_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
            'foreign_language': 1,
            'native_language': 2,
        })

        request.user = user

        resp = EventCreateView().post(request)
        event = Event.objects.all().first()
        response = EventDetailsView().get(request, event.id)

        self.assertEquals(response.status_code, 200)


class SearchEventViewTests(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        self.client.login(username="tester", password="top_secret")

    def test_get_success_without_filter(self):
        response = self.client.get("/events/search/")

        # Checking status code
        self.assertEquals(response.status_code, 200)

        # Assert that a form and a event exists in the context
        self.assertTrue("form" in response.context)
        self.assertTrue("events" in response.context)

        # Assert that we have a field named city and category, and there is choices available
        self.assertTrue(response.context['form'].fields['category'])
        self.assertTrue(response.context['form'].fields['city'])
        self.assertTrue(len(response.context['form'].fields['category'].choices) > 1)
        self.assertTrue(len(response.context['form'].fields['city'].choices) > 1)

        # Check the list of events (quantity of events found)
        self.assertEquals(len(response.context['events']), 4)

    def test_get_success_filter_category(self):
        "Create a test to filter category and "

    def test_get_success_filter_city(self):
        "Create a test to filter category"

    def test_get_success_filter_city_and_category(self):
        "Create a test to filter category"

    def test_get_success_filter_with_no_results(self):
        "Create a test that will return 0 results"