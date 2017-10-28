from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from events.forms import EventForm, Event
from django.views.generic import View
from events.services import PlacesService


class EventEditView(View):
    template_name = "events/create_event.html"
    form_action = "Edit"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request, event_id):
        event = self.get_event_or_404(event_id, request.user.id)

        form = EventForm(instance=event)
        return render(request, self.template_name,
                      {'form': form, 'user': request.user, 'form_action': self.form_action})

    def post(self, request, event_id):
        event = self.get_event_or_404(event_id, request.user.id)

        request = self.places_service.get_city_for_request(request)
        request = self.places_service.get_location_for_request(request)
        request.POST['hosted_by'] = request.user.id

        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully')
            return redirect("edit_event", event_id=event_id)

        return render(request, self.template_name,
                      {'form': form,  'user': request.user, 'form_action': self.form_action})

    @staticmethod
    def get_event_or_404(event_id, user_id):
        event = Event.objects.filter(pk=event_id, hosted_by=user_id).first()
        if not event_id:
            raise Http404()
        return event
