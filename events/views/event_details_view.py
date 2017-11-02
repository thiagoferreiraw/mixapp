from django.shortcuts import render
from django.views.generic import View
from events.forms import Event


class EventDetailsView(View):
    template_name = "events/event_details.html"

    def get(self, request, event_id):
        event_details = Event.objects.filter(id=event_id).first()
        return render(request, self.template_name, {'event_details': event_details})