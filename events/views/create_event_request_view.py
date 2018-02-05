from django.shortcuts import render, redirect
from django.contrib import messages
from events.forms import EventRequestForm
from django.views.generic import View
from events.services import PlacesService


class EventRequestView(View):
    template_name = "events/event_request_form.html"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request):
        form = EventRequestForm()
        return render(request, self.template_name,
                      {'form': form, 'user': request.user, 'form_type': request.GET.get("t", "template")})

    def post(self, request):
        request.POST._mutable = True
        if "city_place_id" in request.POST and request.POST['city_place_id']:
            request = self.places_service.get_city_for_request(request, "city_place_id", "city")

        request.POST['requested_by'] = request.user.id

        form = EventRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event Request created successfully')
            return redirect("request_event_confirmation")

        return render(request, self.template_name,
                      {'form': form,  'user': request.user, 'form_type': request.GET.get("t     ", "template")})

