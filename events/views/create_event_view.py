from django.shortcuts import render, redirect
from django.contrib import messages
from events.forms import EventForm
from django.views.generic import View
from events.services import PlacesService
from users.user_service import UserService
from users.user_enums import UserGroupsEnum


class EventCreateView(View):
    template_name = "events/event_form.html"
    form_action = "Create"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request):
        if not UserService.check_user_permission(request.user.id, UserGroupsEnum.MODERATOR.value):
            return redirect("request_event")

        form = EventForm()
        return render(request, self.template_name,
                      {'form': form, 'user': request.user, 'form_action': self.form_action})

    def post(self, request):
        if not UserService.check_user_permission(request.user.id, UserGroupsEnum.MODERATOR.value):
            return redirect("request_event")

        request = self.places_service.get_city_for_request(request, "city_place_id", "city")
        request = self.places_service.get_location_for_request(request)
        request.POST['hosted_by'] = request.user.id

        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event created successfully')
            return redirect("edit_event_image", event.id)

        return render(request, self.template_name,
                      {'form': form,  'user': request.user, 'form_action': self.form_action})

