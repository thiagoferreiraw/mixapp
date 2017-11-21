from django.test import TestCase, RequestFactory
from mock import patch
from events.models import User, City, Event, Category, Location
from datetime import datetime, timedelta
from events.views.create_event_view import EventCreateView
from events.views.event_details_view import EventDetailsView
from events.views.search_event_view import EventSearchView


class EventsViewsTests(TestCase):
    fixtures = ['categories.json']

    def setUp(self):
        self.factory = RequestFactory()

    @patch('django.contrib.messages.success', return_value=True)
    def test_post_success(self, mock_messages):
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
            'location_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4'
        })

        request.user = user

        response = EventCreateView().post(request)

        self.assertEquals(response.status_code, 302)

        event = Event.objects.all().first()

        self.assertEquals(event.description, "test Event")

        self.assertTrue(mock_messages.called)

        city = City.objects.filter(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4").first()

        self.assertIsNotNone(city.description)

        location = Location.objects.filter(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4").first()

        self.assertIsNotNone(location.description)


class EventDetailsViewsTests(TestCase):
    fixtures = ['categories.json']

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
            'location_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4'
        })

        request.user = user

        resp = EventCreateView().post(request)
        event = Event.objects.all().first()
        response = EventDetailsView().get(request, event.id)

        self.assertEquals(response.status_code, 200)


class SearchEventViewTests(TestCase):
    fixtures = ['fixture_test_events.json']

    def setUp(self):
        self.factory = RequestFactory()

    @patch('django.contrib.messages.success', return_value=True)
    def test_get_success(self, mock_messages):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        Event.objects.all().delete()
        request = self.factory.post("/events/search/", {
            'category': "",
            'city': ""
        })
        request.user = user
        response = EventSearchView().get(request)
        self.assertEquals(response.status_code, 200)
