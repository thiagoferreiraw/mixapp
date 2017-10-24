from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from events.forms import EventCreateForm
from django.views.generic import View


class EventCreateView(View):
    template_name = "events/create_event.html"

    def get(self, request):
        form = EventCreateForm()
        return render(request, self.template_name,
                      {'form': form, 'user': request.user})

    def post(self, request):
        form = EventCreateForm(request.POST)
        if form.is_valid():
            form.save(user_id=request.user.id, google_city_id="ChIJHcKsaB2_uZQROerevgruuDc")
            messages.success(request,'Event created successfully')
            return redirect("create_event")

        return render(request, self.template_name,
                      {'form': form,  'user': request.user})