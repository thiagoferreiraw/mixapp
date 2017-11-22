from django.test import TestCase
from events.services import PlacesService
from events.models import User, Event
from datetime import datetime, timedelta
from events.views.create_event_view import EventForm


class EventsFormsTests(TestCase):
    fixtures = ['categories.json', 'languages.json']

    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

    def test_insert_form_success(self):

        city = PlacesService().get_and_save_city("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        location = PlacesService().get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")

        date_time_form = (datetime.now() + timedelta(days=10))

        form = EventForm({
            'name': "Test Event",
            'description': "test Event",
            'duration': 1,
            'date': date_time_form.date(),
            'time': date_time_form.time(),
            'city': city.id,
            'location': location.id,
            "location_lat": -33.8688,
            "location_lng": 151.2195,
            'expected_costs': 200,
            'hosted_by': self.user.id,
            'category': 1,
            'foreign_language': 1,
            'native_language': 2,

        })

        self.assertTrue(form.is_valid())

        event = form.save()

        self.assertEquals(event.name, "Test Event")
        self.assertEquals(event.description, "test Event")
        self.assertEquals(event.duration, 1)
        self.assertTrue(event.date is not None)
        self.assertTrue(event.time is not None)
        self.assertEquals(event.city.id, city.id)
        self.assertEquals(event.location.id, location.id)
        self.assertEquals(event.expected_costs, 200)
        self.assertEquals(event.hosted_by_id, self.user.id)

    def test_insert_form_fail_invalid_date(self):

        city = PlacesService().get_and_save_city("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        location = PlacesService().get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")

        form = EventForm({
            'name': "Test Event",
            'description': "test Event",
            'duration': 1,
            'date': "2017-01-01",
            'time': "15:00",
            'city': city.id,
            "location_lat": -33.8688,
            "location_lng": 151.2195,
            'location': location.id,
            'expected_costs': 200,
            'hosted_by': self.user.id,
            'category': 1,
            'foreign_language': 1,
            'native_language': 2,
        })

        self.assertFalse(form.is_valid())
        self.assertTrue("date" in form.errors)

    def test_insert_form_fail_invalid_time(self):

        city = PlacesService().get_and_save_city("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        location = PlacesService().get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")

        date_time_form = (datetime.now() + timedelta(minutes=-1))

        form = EventForm({
            'name': "Test Event",
            'description': "test Event",
            'duration': 1,
            'date': date_time_form.date(),
            'time': date_time_form.time(),
            'city': city.id,
            "location_lat": -33.8688,
            "location_lng": 151.2195,
            'location': location.id,
            'expected_costs': 200,
            'hosted_by': self.user.id,
            'category': 1,
            'foreign_language': 1,
            'native_language': 2,

        })

        self.assertFalse(form.is_valid())
        self.assertTrue("time" in form.errors)

    def test_insert_form_fail(self):
        form = EventForm({
            'description': "test Event",
            'duration': 1,
            'date_time': datetime.now().strftime("%Y-%m-%d"),
            'city': None,
            'location': "Location",
            "location_lat": -33.8688,
            "location_lng": 151.2195,
            'expected_costs': 200,
            'hosted_by': None,
            'category': [],
            'foreign_language': 1,
            'native_language': 2,
        })

        self.assertFalse(form.is_valid())
        self.assertTrue("name" in form.errors)

    def test_edit_form_success(self):
        city = PlacesService().get_and_save_city("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        location = PlacesService().get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")

        event = Event(name="Test Event", description="test Event", duration=1,
                      date=datetime.now().date(), time=datetime.now().time(),
                      city_id=city.id, location_id=location.id, expected_costs=200,
                      hosted_by_id=self.user.id, category_id=1, location_lat=0, location_lng=0,
                      foreign_language_id=1, native_language_id=1)
        event.save()

        date_time_form = (datetime.now() + timedelta(days=10))

        form = EventForm({
            'name': "Edit Test Event",
            'description': "test Event",
            'duration': 1,
            'date': date_time_form.date(),
            'time': date_time_form.time(),
            'city': city.id,
            "location_lat": -33.8688,
            "location_lng": 151.2195,
            'location': location.id,
            'expected_costs': 200,
            'hosted_by': self.user.id,
            'category': 1,
            'foreign_language': 1,
            'native_language': 2,
        }, instance=event)
        form.is_valid()
        print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())




