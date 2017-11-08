from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import View
from events.forms import Event


class EventDetailsView(View):
    template_name = "events/event_details.html"

    def get(self, request, event_id):
        event_details = self.get_event_or_404(event_id)
        
        return render(request, self.template_name, {'event_details': event_details})

    @staticmethod
    def get_event_or_404(event_id):
        event = Event.objects.filter(pk=event_id).first()
        if not event:
            raise Http404()
        return event