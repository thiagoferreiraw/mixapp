from django.shortcuts import render, redirect
from django.contrib import messages
from events.forms import EventForm
from django.views.generic import View
from events.services import PlacesService


class EventCreateView(View):
    template_name = "events/create_event.html"
    form_action = "Create"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request):

        form = EventForm()
        return render(request, self.template_name,
                      {'form': form, 'user': request.user, 'form_action': self.form_action})

    def post(self, request):

        request = self.places_service.get_city_for_request(request)
        request = self.places_service.get_location_for_request(request)
        request.POST['hosted_by'] = request.user.id

        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully')
            return redirect("create_event")

        return render(request, self.template_name,
                      {'form': form,  'user': request.user, 'form_action': self.form_action})

