from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from users.forms import UserInvitationForm
from django.views.generic import View
from users.models import SignupInvitation
from django.core.mail import send_mail


class UserInvitationView(View):
    template_name = "registration/send_invitation.html"

    def get(self, request):
        form = UserInvitationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserInvitationForm(request.POST)
        if form.is_valid():
            invited = SignupInvitation()
            invited.email_invited = form.data['email_invited']
            invited.invited_by = User.objects.get(pk=request.user.id)
            invited.save()
            link = '/signup/{1}'.format(invited.hash)
            send_mail('Brigid Mixs Invitation', 'Congrats for invitation!\nSignup in: {0}'.format(link), 'noreply@brigidmixs.org', [invited.email_invited])
            messages.success(request, "Invitation sent successfully!")

            invitations = SignupInvitation.objects.filter(invited_by=request.user)
            return render(request, self.template_name, {'invitations': invitations, 'form': form})

        return render(request, self.template_name, {'form': form})