from django.shortcuts import render
from django.contrib import messages
from users.forms import UserWaitingListForm
from django.views.generic import View


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