from django.test import TestCase, RequestFactory
from users.models import *
from users.models import User
from users.forms import UserCreationForm, UserWaitingListForm, UserInvitationForm


class TestForms(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        User.objects.all().delete()

    def test_form_user_signup_duplicated_email(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        form = UserCreationForm({
            "email": "tester@tester.com",
            "first_name": "Tester1",
            "last_name": "Tester2",
            "password1": "123",
            "password2": "123",
            "username": "testerx",
        })

        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)

    def test_form_user_signup_duplicated_username(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')

        form = UserCreationForm({
            "email": "tester@tester.com",
            "first_name": "Tester1",
            "last_name": "Tester2",
            "password1": "123",
            "password2": "123",
            "username": "tester",
        })

        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_form_user_waiting_list(self):
        form = UserWaitingListForm({'email': 'tester@mail.com'})
        self.assertTrue(form.is_valid())
        waiting_list = form.save()
        self.assertEqual(waiting_list.email, 'tester@mail.com')

    def test_form_user_waiting_list_duplicated(self):
        SignupWaitingList(email="tester@mail.com").save()

        form = UserWaitingListForm({'email': 'tester@mail.com'})
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)

    def test_form_send_invitation_valid(self):
        form = UserInvitationForm({'email_invited': 'tester@mail.com'})
        self.assertTrue(form.is_valid())
        send_invitation = form.save()
        self.assertEqual(send_invitation.email_invited, 'tester@mail.com')

    def test_form_send_invitation_invalid(self):
        form = UserInvitationForm({'email_invited': ''})
        self.assertFalse(form.is_valid())
