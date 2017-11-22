from django.test import TestCase, RequestFactory
from mock import patch
from users.models import *
from users.views.user_edit_profile_view import UserEditProfileView


class TestViews(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        User.objects.all().delete()

    def test_get_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_post_login_page(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        response = self.client.post('/login/', {'username': "tester", 'password': 'top_secret'})
        self.assertRedirects(response, "/events/search/")

    def test_post_login_page_with_email(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        response = self.client.post('/login/', {'username': "tester@tester.com", 'password': 'top_secret'})
        self.assertRedirects(response, "/events/search/")

    def test_post_login_page_with_failing_email(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        response = self.client.post('/login/', {'username': "wrong_email@tester.com", 'password': 'top_secret'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_get_settings_page(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        self.client.login(username='tester', password='top_secret')
        response = self.client.get('/user/settings/')
        self.assertEqual(response.status_code, 200)

    def test_get_settings_password(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        self.client.login(username='tester', password='top_secret')
        response = self.client.get('/user/settings/password/')
        self.assertEqual(response.status_code, 200)

    def test_post_settings_password(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        self.client.login(username='tester', password='top_secret')
        response = self.client.post('/user/settings/password/', {'old_password': 'top_secret', 'new_password1': 'top_secret2', 'new_password2': 'top_secret2'} )
        self.assertRedirects(response, '/user/settings/password/')

    def test_access_to_home_page_without_logged_user(self):
        response = self.client.get('/home/', follow=True)
        self.assertRedirects(response, '/login/?next=/home/')

    def test_access_to_edit_profile_without_logged_user(self):
        response = self.client.get('/user/profile/', follow=True)
        self.assertRedirects(response, '/login/?next=/user/profile/')

    def test_get_access_signup_page_with_invalid_invitation(self):
        response = self.client.get('/signup/invalid_hash/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['hash'], 'invalid_hash')

    def test_post_signup_page_with_invalid_invitation(self):
        response = self.client.post('/signup/invalid_hash/', {})

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
            "first_name": "Tester1",
            "last_name": "Tester2",
            "password1": "123",
            "password2": "123",
            "username": "tester"
        })

        self.assertRedirects(response, "/home/")

        created_user = User.objects.filter(username="tester")[0]

        self.assertEqual(created_user.email, "invited@test.com")
        self.assertEqual(created_user.first_name, "Tester1")
        self.assertEqual(created_user.last_name, "Tester2")
        self.assertEqual(created_user.username, "tester")

        signup_invitation = SignupInvitation.objects.get(pk=signup_invitation.id)

        self.assertTrue(signup_invitation.user_has_signed_up)

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

    def test_get_user_categories(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        categories = []
        for i in range(5):
            categories.append(Category(name="Cat {}".format(i), description="cat"))
            categories[len(categories)-1].save()

        UserCategory(user_id_id=user.id, category_id_id=categories[0].id).save()

        user_categories = UserEditProfileView._get_user_categories(user.id)

        self.assertEqual(len(user_categories), 5)

        chosen_categories = list(filter(lambda x: x['selected'], user_categories))

        self.assertEqual(chosen_categories[0]['id'], categories[0].id)
        self.assertEqual(chosen_categories[0]['name'], categories[0].name)
        self.assertEqual(chosen_categories[0]['selected'], True)

    def test_post_signup_page_with_valid_invitation_success_with_categories(self):
        categories = []
        for i in range(5):
            categories.append(Category(name="Cat {}".format(i), description="cat"))
            categories[len(categories)-1].save()

        signup_invitation = SignupInvitation(email_invited="invited@test.com")
        signup_invitation.save()

        signup_url = '/signup/{}/'.format(signup_invitation.hash).replace("-", "")

        response = self.client.post(signup_url, {
            "email": "invited@test.com",
            "first_name": "Tester1",
            "last_name": "Tester2",
            "password1": "123",
            "password2": "123",
            "username": "tester",
            "categories": [categories[0].id, categories[1].id]
        })

        self.assertRedirects(response, "/home/")

        created_user = User.objects.filter(username="tester")[0]

        self.assertEqual(created_user.email, "invited@test.com")
        self.assertEqual(created_user.first_name, "Tester1")
        self.assertEqual(created_user.last_name, "Tester2")
        self.assertEqual(created_user.username, "tester")

        chosen_categories = UserCategory.objects.filter(user_id_id=created_user.id)
        self.assertEqual(len(chosen_categories), 2)

    def test_get_edit_user_profile(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        self.client.login(username="tester", password="top_secret")

        response = self.client.get("/user/profile/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("form" in response.context)

    @patch('django.contrib.messages.success', return_value=True)
    def test_post_edit_profile_success(self, mock_messages):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        self.client.login(username="tester", password="top_secret")

        response = self.client.post("/user/profile/", {
            "email": "invited@test.com",
            "first_name": "Tester changed1",
            "last_name": "Tester changed2",
        })

        self.assertEqual(response.url, "/user/profile/")
        self.assertEqual(response.status_code, 302)

        updated_user = User.objects.filter(username="tester")[0]

        self.assertEqual(updated_user.first_name, "Tester changed1")
        self.assertEqual(updated_user.last_name, "Tester changed2")
        self.assertTrue(mock_messages.called)

    @patch('django.contrib.messages.success', return_value=True)
    def test_post_edit_profile_failed(self, mock_messages):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        self.client.login(username="tester", password="top_secret")

        response = self.client.post("/user/profile/", {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue("first_name" in response.context['form'].errors)

    def test_post_waiting_list_success(self):
        response = self.client.post('/waiting_list/', {
            "email": "tester@test.com",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/waiting_list/")

        signup_waiting_list = SignupWaitingList.objects.filter(email="tester@test.com")

        self.assertTrue(len(signup_waiting_list) > 0)

    def test_post_waiting_list_fail(self):
        response = self.client.post('/waiting_list/', {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue("email" in response.context['form'].errors)

    def test_get_waiting_list(self):
        response = self.client.get('/waiting_list/')
        self.assertEqual(response.status_code, 200)

    def test_post_send_invitation_success(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        self.client.login(username="tester", password="top_secret")

        response = self.client.post('/user/send_invitation/', {
            "email_invited": "invited@test.com",
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user/send_invitation/")

        invitation_created = SignupInvitation.objects.filter(email_invited="invited@test.com")

        self.assertTrue(len(invitation_created) > 0)

    def test_post_send_invitation_fail(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        self.client.login(username="tester", password="top_secret")

        response = self.client.post('/user/send_invitation/', {})

        self.assertEqual(response.status_code, 200)
        self.assertTrue("email_invited" in response.context['form'].errors)

    def test_get_send_invitation(self):
        User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        self.client.login(username="tester", password="top_secret")

        response = self.client.get('/user/send_invitation/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue("invitations" in response.context)


