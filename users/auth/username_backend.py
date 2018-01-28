from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class UsernameBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username__iexact=username)

            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        except User.DoesNotExist:
            return None

        return None