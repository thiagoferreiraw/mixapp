from django.test import TestCase, RequestFactory
from users import views
from unittest import mock

class UserTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_login_page(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_access_to_home_page_without_logged_user(self):
        response = self.client.get('/home/', follow=True)
        self.assertRedirects(response, '/login/?next=/home/')

    def test_signup_with_invalid_invitation(self):
        response = self.client.get('/signup/invalid_hash/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['hash'], 'invalid_hash')



