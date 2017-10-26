from django.shortcuts import render, redirect
from django.contrib import messages
from events.forms import EventCreateForm
from django.views.generic import View
from events.services import PlacesService


class EventCreateView(View):
    template_name = "events/create_event.html"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request):

        form = EventCreateForm(initial={
            'name': "Test Event",
            'description': "test Event",
            'duration': 1,
            'date': "2017-01-01",
            'time': "15:00",
            'expected_costs': 200,
            #'hosted_by': user.id,
            'category': 1,
            #'city_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4',
            #'location_place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4'
        })
        return render(request, self.template_name,
                      {'form': form, 'user': request.user})

    def post(self, request):

        request = self.get_city(request)
        request = self.get_location(request)
        request.POST['hosted_by'] = request.user.id

        form = EventCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully')
            return redirect("create_event")

        return render(request, self.template_name,
                      {'form': form,  'user': request.user})

    def get_city(self, request):
        if not (request.POST['city_place_id'] is None or request.POST['city_place_id'] == ""):
            city = self.places_service.get_and_save_city(request.POST['city_place_id'], "en")
            request.POST._mutable = True
            request.POST['city'] = city.id
        return request

    def get_location(self, request):
        if request.POST['location_place_id'] is not None and request.POST['location_place_id'] != "":
            location = self.places_service.get_and_save_location(request.POST['location_place_id'], "en")
            request.POST._mutable = True
            request.POST['location'] = location.id
        return request