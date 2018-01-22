from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

from events.models import Language
from events.services import PlacesService
from users.models import SignupInvitation
from django.views.generic import View
from users.forms import UserCreationForm, ProfileForm
from users.models import Category
from django.contrib.auth.models import User

class UserSignupView(View):
    template_name = "registration/signup.html"
    redirect_to = "home"

    def __init__(self):
        self.places_service = PlacesService()

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
        profile_form = ProfileForm()
        return render(request, self.template_name, {'form': form, 'profile_form': profile_form,
                                                    'categories': Category.objects.all(),
                                                    'languages': Language.objects.all(),
                                                    'invitation': signup_invitation})

    def post(self, request, invitation_hash):
        signup_invitation = self.get_invitation(request, invitation_hash)
        if not signup_invitation:
            return render(request, 'registration/invalid_signup.html', {'hash': invitation_hash})

        request = self.places_service.get_city_for_request(request, 'birth_city_place_id', 'birth_city')
        request = self.places_service.get_city_for_request(request, 'current_city_place_id', 'current_city')

        form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if request.POST.get("email") != signup_invitation.email_invited:
            messages.error(request,
                           "You must sign up with the invited email: {}".format(signup_invitation.email_invited))
            return render(request, self.template_name,
                          {'form': form, 'profile_form': profile_form,
                           'categories': Category.objects.all(), 'languages': Language.objects.all(),
                           'invitation': signup_invitation})

        if form.is_valid():
            user = form.save(chosen_categories=request.POST.getlist('categories'), chosen_languages=request.POST.getlist('languages'), signup_invitation=signup_invitation)
            profile_form = ProfileForm(request.POST, instance=user.profile)

            if profile_form.is_valid():
                profile_form.save()
                user = authenticate(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1')
                )
                login(request, user)

                return redirect(self.redirect_to)
            else:
                user.delete()

        return render(request, self.template_name,
                      {'form': form, 'profile_form': profile_form,
                       'categories': Category.objects.all(), 'languages': Language.objects.all(),
                       'invitation': signup_invitation})
