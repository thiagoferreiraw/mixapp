from django.contrib.auth.models import Group
from django.test import TestCase
from users.models import *
from users.user_enums import UserGroupsEnum
from users.user_service import UserService


class TestService(TestCase):
    fixtures = ['user_groups']

    def setUp(self):
        User.objects.all().delete()

    def test_check_user_permission_should_return_true(self):
        user = User.objects.create_user(username='tester', email='tester@tester.com', password='top_secret')
        group = Group.objects.get(name=UserGroupsEnum.MODERATOR.value)
        user.groups.add(group)  # Moderator group
        user.save()

        result = UserService.check_user_permission(user.id, UserGroupsEnum.MODERATOR.value)

        self.assertTrue(result)

    def test_check_user_permission_should_return_false(self):
        user = User.objects.create_user(username='tester_2', email='tester@tester.com', password='top_secret')

        result = UserService.check_user_permission(user.id, UserGroupsEnum.MODERATOR.value)

        self.assertFalse(result)

    def test_check_user_permission_should_return_false_group_does_not_exist(self):
        user = User.objects.create_user(username='tester_2', email='tester@tester.com', password='top_secret')
        group = Group.objects.get(name=UserGroupsEnum.MODERATOR.value)
        user.groups.add(group)  # Moderator group

        result = UserService.check_user_permission(user.id, "RANDOM_GROUP")

        self.assertFalse(result)
