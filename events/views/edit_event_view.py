from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from events.forms import EventForm, Event
from django.views.generic import View
from events.services import PlacesService
from users.user_enums import UserGroupsEnum
from users.user_service import UserService


class EventEditView(View):
    template_name = "events/event_form.html"
    form_action = "Edit"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request, event_id):
        if not UserService.check_user_permission(request.user.id, UserGroupsEnum.MODERATOR.value):
            return redirect("request_event")

        event = self.get_event_or_404(event_id, request.user.id)

        form = EventForm(instance=event)
        return render(request, self.template_name,
                      {'form': form, 'user': request.user, 'form_action': self.form_action, 'event_id': event_id})

    def post(self, request, event_id):
        if not UserService.check_user_permission(request.user.id, UserGroupsEnum.MODERATOR.value):
            return redirect("request_event")

        event = self.get_event_or_404(event_id, request.user.id)

        request = self.places_service.get_city_for_request(request, "city_place_id", "city")
        request = self.places_service.get_location_for_request(request)

        request.POST['hosted_by'] = request.user.id

        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event updated successfully')

            if "location_lat" in form.changed_data or "location_lng" in form.changed_data:
                return redirect("edit_event_image", event.id)

            return redirect("list_events")

        return render(request, self.template_name,
                      {'form': form,  'user': request.user, 'form_action': self.form_action, 'event_id': event_id})

    @staticmethod
    def get_event_or_404(event_id, user_id):
        event = Event.objects.filter(pk=event_id, hosted_by=user_id).first()
        if not event:
            raise Http404()
        return event
