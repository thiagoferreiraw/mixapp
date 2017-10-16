from django.test import TestCase, RequestFactory
from users.models import SignupInvitation
from users.models import User


class UserTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        User.objects.all().delete()

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

    def test_post_signup_page_with_valid_invitation_blank_form(self):
        signup_invitation = SignupInvitation(email_invited="invited@test.com")
        signup_invitation.save()

        signup_url = '/signup/{}/'.format(signup_invitation.hash).replace("-", "")

        response = self.client.post(signup_url, {})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['invitation'], signup_invitation)
        self.assertTrue("username" in response.context['form'].errors)
        self.assertTrue("password1" in response.context['form'].errors)
        self.assertTrue("password2" in response.context['form'].errors)
        self.assertTrue("first_name" in response.context['form'].errors)
        self.assertTrue("last_name" in response.context['form'].errors)
        self.assertTrue("email" in response.context['form'].errors)

    def test_post_signup_page_with_valid_invitation_success(self):
        signup_invitation = SignupInvitation(email_invited="invited@test.com")
        signup_invitation.save()

        signup_url = '/signup/{}/'.format(signup_invitation.hash).replace("-", "")

        response = self.client.post(signup_url, {
            "email": "invited@test.com",
            "first_name": "Tester",
            "last_name": "Tester",
            "password1": "123",
            "password2": "123",
            "username": "tester"
        })

        self.assertRedirects(response, "/home/")

        created_user = User.objects.filter(username="tester")[0]

        self.assertIsNotNone(created_user)

    def test_post_signup_page_with_valid_invitation_email_different_from_invite(self):
        signup_invitation = SignupInvitation(email_invited="invited@test.com")
        signup_invitation.save()

        signup_url = '/signup/{}/'.format(signup_invitation.hash).replace("-", "")

        response = self.client.post(signup_url, {
            "email": "other_email@test.com",
            "first_name": "Tester",
            "last_name": "Tester",
            "password1": "123",
            "password2": "123",
            "username": "tester"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['invitation'], signup_invitation)

        context_messages = list(response.context['messages'])

        self.assertEqual(len(context_messages), 1)
        self.assertEqual(str(context_messages[0]), "You must sign up with the invited email: invited@test.com")

