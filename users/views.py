from users.models import Category
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.contrib import messages

from users.forms import UserCreationForm, UserEditProfileForm


def index(request):
      return render(request, "../templates/pages/index.html", {})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form, 'categories': Category.objects.all()})

@login_required
def home(request):
    return render(request, 'user_profile/home.html')

@login_required
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'user_profile/settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'user_profile/password.html', {'form': form})

def edit_profile(request):
    categories = Category.objects.all()
    categories = map(lambda cat: {'id': cat.id, 'name': cat.name, 'selected': False}, categories)

    user = User.objects.get(pk=request.user.id)

    if request.method == 'POST':
        form = UserEditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, '{}, your profile has been updated successfully'.format(request.POST['first_name']))
            return redirect("edit_profile")
    else:
        form = UserEditProfileForm(instance=user)


    return render(request, 'user_profile/profile.html', {'form': form, 'categories': categories, 'username': request.user.username})

