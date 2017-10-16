from django.test import TestCase, RequestFactory
from users.models import SignupInvitation


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

    def test_get_access_signup_pagewith_invalid_invitation(self):
        response = self.client.get('/signup/invalid_hash/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['hash'], 'invalid_hash')

    def test_get_signup_page_with_valid_invitation(self):
        signup_invitation = SignupInvitation(email_invited="invited@test.com")
        signup_invitation.save()

        signup_url = '/signup/{}/'.format(signup_invitation.hash).replace("-", "")

        response = self.client.get(signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['invitation'], signup_invitation)

    def test_post_signup_page_with_valid_invitation(self):
        signup_invitation = SignupInvitation(email_invited="invited@test.com")
        signup_invitation.save()

        signup_url = '/signup/{}/'.format(signup_invitation.hash).replace("-", "")

        response = self.client.post(signup_url, {'email': 'invited@test.com',
                                    })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['invitation'], signup_invitation)
