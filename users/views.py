from users.models import Category, UserCategory
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.contrib import messages
from users.models import SignupInvitation
from users.forms import UserCreationForm, UserEditProfileForm, UserWaitingListForm
from django.views.generic import View


class UserSignupView(View):
    template_name = "registration/signup.html"
    redirect_to = "home"

    @staticmethod
    def get_invitation(request, invitation_hash):
        try:
            signup_invitation = SignupInvitation.objects.filter(hash=invitation_hash, user_has_signed_up=False)[0]
        except (ValueError, IndexError) as e:
            return None
        return signup_invitation

    def get(self, request, invitation_hash):
        signup_invitation = self.get_invitation(request, invitation_hash)
        if not signup_invitation:
            return render(request, 'registration/invalid_signup.html', {'hash': invitation_hash})

        form = UserCreationForm(initial={'email': signup_invitation.email_invited})
        return render(request, self.template_name, {'form': form, 'categories': Category.objects.all(),
                                                    'invitation': signup_invitation})

    def post(self, request, invitation_hash):
        signup_invitation = self.get_invitation(request, invitation_hash)
        if not signup_invitation:
            return render(request, 'registration/invalid_signup.html', {'hash': invitation_hash})

        form = UserCreationForm(request.POST)

        if request.POST.get("email") != signup_invitation.email_invited:
            messages.error(request,
                           "You must sign up with the invited email: {}".format(signup_invitation.email_invited))
            return render(request, self.template_name,
                          {'form': form, 'categories': Category.objects.all(), 'invitation': signup_invitation})

        if form.is_valid():
            form.save(chosen_categories=request.POST.getlist('categories'), signup_invitation=signup_invitation)
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)

            return redirect(self.redirect_to)


class UserEditProfileView(View):
    template_name = "user_profile/profile.html"

    def get(self, request):
        categories = _get_user_categories(request.user.id)
        form = UserEditProfileForm(instance=User.objects.get(pk=request.user.id))
        return render(request, self.template_name,
                      {'form': form, 'categories': categories, 'user': request.user})

    def post(self, request):
        form = UserEditProfileForm(request.POST, instance=User.objects.get(pk=request.user.id))
        if form.is_valid():
            form.save(chosen_categories=request.POST.getlist('categories'))
            messages.success(request,
                             'Your profile has been updated successfully'.format(request.POST['first_name']))
            return redirect("edit_profile")

        categories = _get_user_categories(request.user.id)

        return render(request, self.template_name,
                      {'form': form, 'categories': categories, 'user': request.user})

class UserWaitingListView(View):
    template_name = "registration/waiting_list_signup.html"

    def get(self, request):
        form = UserWaitingListForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserWaitingListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You've been added to our waiting list! Looking forward to see you again :)")

        return render(request, self.template_name, {'form': form})

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


def _get_user_categories(user_id):
    categories = Category.objects.all()
    categories = map(lambda cat: {'id': cat.id, 'name': cat.name, 'selected': False}, categories)

    user_categories = UserCategory.objects.filter(user_id_id=user_id)

    if user_categories:
        categories_ids = [cat.category_id_id for cat in user_categories]
        categories = list(
            map(lambda cat: {'id': cat['id'], 'name': cat['name'], 'selected': cat['id'] in categories_ids},
                categories))

    return categories