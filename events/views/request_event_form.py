from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from events.services import PlacesService


class RequestEventView(View):
    template_name = "events/request_event_form.html"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request):
        return render(request, self.template_name, {'user': request.user})

