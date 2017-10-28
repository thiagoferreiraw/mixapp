from django.shortcuts import render, redirect
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
        invitations = SignupInvitation.objects.filter(invited_by=request.user)
        return render(request, self.template_name, {'invitations': invitations, 'form': form})

    def post(self, request):
        form = UserInvitationForm(request.POST)
        if form.is_valid():
            invited = form.save()
            invited.invited_by = User.objects.get(pk=request.user.id)
            invited.save()

            protocol = 'https' if request.is_secure() else 'http'
            domain = request.META['HTTP_HOST'] if "HTTP_HOST" in request.META else "localhost"
            link = '{0}://{1}/signup/{2}'.format(protocol, domain, invited.hash)
            send_mail('Brigid Mixs Invitation', 'Congrats for invitation!\nSignup in: {0}'.format(link), 'noreply@brigidmixs.org', [invited.email_invited])
            messages.success(request, "Invitation sent successfully!")
            return redirect("send_invitation")

        invitations = SignupInvitation.objects.filter(invited_by=request.user)
        return render(request, self.template_name, {'form': form, 'invitations': invitations})
