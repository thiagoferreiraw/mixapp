from django.contrib.auth.views import login
from users.models import User
from django.core.validators import validate_email


def login_view(request):
    if request.method == "POST":

        # Verify weather the user is trying to login with username or email
        if is_email(request.POST['username']):
            username = get_username_by_email(request.POST['username'])
            if username:
                request.POST._mutable = True
                request.POST['username'] = username

    print(request.POST)

    return login(request)


def get_username_by_email(email):
    user = User.objects.filter(email=email).first()
    if user:
        return user.username
    return None


def is_email(value):
    try:
        validate_email(value)
        return True
    except Exception as e:
        return False