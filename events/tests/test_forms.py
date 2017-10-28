from django.test import TestCase
from events.services import PlacesService
from events.models import User, Category, Event
from datetime import datetime
from events.views.create_event_view import EventForm


class EventsFormsTests(TestCase):
    fixtures = ['categories.json']

    def test_insert_form_success(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        city = PlacesService().get_and_save_city("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        location = PlacesService().get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")

        form = EventForm({
            'name': "Test Event",
            'description': "test Event",
            'duration': 1,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'time': "15:00",
            'city': city.id,
            'location': location.id,
            'expected_costs': 200,
            'hosted_by': user.id,
            'category': 1
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
        self.assertEquals(event.hosted_by_id, user.id)

    def test_insert_form_fail(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        form = EventForm({
            'description': "test Event",
            'duration': 1,
            'date_time': datetime.now().strftime("%Y-%m-%d"),
            'city': None,
            'location': "Location",
            'expected_costs': 200,
            'hosted_by': None,
            'category': []
        })

        self.assertFalse(form.is_valid())
        self.assertTrue("name" in form.errors)

    def test_edit_form_success(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        city = PlacesService().get_and_save_city("ChIJHcKsaB2_uZQROerevgruuDc", "en")
        location = PlacesService().get_and_save_location("ChIJHcKsaB2_uZQROerevgruuDc", "en")

        event = Event(name="Test Event", description="test Event", duration=1,
                      date=datetime.now().strftime("%Y-%m-%d"), time="15:00",
                      city_id=city.id, location_id=location.id, expected_costs=200,
                      hosted_by_id=user.id, category_id=1)
        event.save()

        form = EventForm({
            'name': "Edit Test Event",
            'description': "test Event",
            'duration': 1,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'time': "15:00",
            'city': city.id,
            'location': location.id,
            'expected_costs': 200,
            'hosted_by': user.id,
            'category': 1
        }, instance=event)

        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())




