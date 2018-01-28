from django.contrib.auth.views import login
from users.models import User
from django.core.validators import validate_email


def login_view(request):
    return login(request)