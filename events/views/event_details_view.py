from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from events.forms import Event


class EventDetailsView(View):
    template_name = "events/event_details.html"

    def get(self, request, event_id):
        event_details = get_object_or_404(Event, pk=event_id)
        return render(request, self.template_name, {'event_details': event_details})