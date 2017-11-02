from django.shortcuts import render, redirect
from django.http import Http404
from events.forms import Event
from django.views.generic import View
from events.services import PlacesService
from events.models import LocationImage


class ChooseImageView(View):
    template_name = "events/choose_image.html"
    form_action = "Edit"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request, event_id):
        event = self.get_event_or_404(event_id, request.user.id)

        if "image_id" in request.GET:
            image = self.get_image_or_404(request.GET['image_id'])
            event.image_url = image.url
            event.save()
            return redirect("list_events")

        images = LocationImage.objects.filter(location_id=event.location.id).order_by('-id')
        return render(request, self.template_name,
                      {'images': images})

    @staticmethod
    def get_event_or_404(event_id, user_id):
        event = Event.objects.filter(pk=event_id, hosted_by=user_id).first()
        if not event_id:
            raise Http404()
        return event

    @staticmethod
    def get_image_or_404(image_id):
        event = LocationImage.objects.filter(pk=image_id).first()
        if not event:
            raise Http404()
        return event
