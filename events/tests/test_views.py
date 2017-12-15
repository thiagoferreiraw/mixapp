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
            'template': 1,
            'duration': 1,
            'date': (datetime.now() + timedelta(days=1)).date(),
            'time': datetime.now().time(),
            'expected_costs': 200,
            'hosted_by': self.user.id,
            "location_lat": "-33.8688",
            "location_lng": "151.2195",
            'city_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
            'location_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
            'foreign_language': 1,
            'native_language': 2,
        })

        self.assertEquals(response.status_code, 302)

        event = Event.objects.all().order_by('-id').first()

        self.assertEqual(response.url, "/events/edit/{}/image/".format(event.id))

        self.assertEquals(event.template.id, 1)

        self.assertTrue(mock_messages.called)

        city = City.objects.filter(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4").first()

        self.assertIsNotNone(city.description)

        location = Location.objects.filter(place_id="ChIJN1t_tDeuEmsRUsoyG83frY4").first()

        self.assertIsNotNone(location.description)


class EventDetailsViewsTests(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client.login(username="admin", password="123")

    def test_get_success(self):
        response = self.client.get("/events/details/1")
        self.assertEquals(response.status_code, 200)

    def test_get_not_found(self):
        response = self.client.get("/events/details/99")
        self.assertEquals(response.status_code, 404)

class SearchEventViewTests(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client.login(username="admin", password="123")

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
        response = self.client.get("/events/search/?city=&category=1")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTrue("events" in response.context)
        self.assertEquals(len(response.context['events']), 1)

    def test_get_success_filter_city(self):
        response = self.client.get("/events/search/?city=1&category=")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTrue("events" in response.context)
        self.assertEquals(len(response.context['events']), 1)

    def test_get_success_filter_city_and_category(self):
        response = self.client.get("/events/search/?city=1&category=1")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTrue("events" in response.context)
        self.assertEquals(len(response.context['events']), 1)

    def test_get_success_filter_with_no_results(self):
        response = self.client.get("/events/search/?city=99&category=1")

        self.assertEquals(response.status_code, 200)
        self.assertTrue("form" in response.context)
        self.assertTrue("events" in response.context)
        self.assertEquals(len(response.context['events']), 0)

    def test_get_with_invalid_category(self):
        response = self.client.get("/events/search/?city=1&category=99")

        self.assertTrue(response.context['form'].errors)

    def test_get_with_invalid_city(self):
        response = self.client.get("/events/search/?city=99&category=1")

        self.assertTrue(response.context['form'].errors)


class EventTemplateViewTests(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client.login(username="admin", password="123")

    def test_get_create_success(self):
        response = self.client.get("/events/templates/new/")
        self.assertEquals(response.status_code, 200)

    def test_get_edit_success(self):
        response = self.client.get("/events/templates/edit/1/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("form" in response.context)

    def test_get_list_success(self):
        response = self.client.get("/events/templates/list/")
        self.assertEquals(response.status_code, 200)
        self.assertTrue("templates" in response.context)
        self.assertTrue(len(response.context["templates"]) > 0)

    def test_post_create_success(self):
        response = self.client.post("/events/templates/new/",
                                   {"name": "new template", "category": 1, "description": "test"})
        self.assertRedirects(response, "/events/templates/list/")

    def test_post_edit_success(self):
        response = self.client.post("/events/templates/edit/1/",
                                   {"name": "new template", "category": 1, "description": "test"})
        self.assertRedirects(response, "/events/templates/list/")