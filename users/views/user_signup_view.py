from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

from events.models import Language
from users.models import SignupInvitation
from django.views.generic import View
from users.forms import UserCreationForm
from users.models import Category


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
                                                    'languages': Language.objects.all(),
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
                          {'form': form, 'categories': Category.objects.all(), 'languages': Language.objects.all(), 'invitation': signup_invitation})

        if form.is_valid():
            form.save(chosen_categories=request.POST.getlist('categories'), chosen_languages=request.POST.getlist('languages'), signup_invitation=signup_invitation)
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)

            return redirect(self.redirect_to)