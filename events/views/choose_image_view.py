from django.shortcuts import render, redirect
from django.http import Http404
from events.forms import Event
from django.views.generic import View
from events.services import PlacesService
from events.forms import ImageUploadForm
from django.contrib import messages
import uuid


class ChooseImageView(View):
    template_name = "events/choose_image.html"
    form_action = "Edit"

    def __init__(self):
        self.places_service = PlacesService()

    def get(self, request, event_id):
        event = self.get_event_or_404(event_id, request.user.id)

        images = self.places_service.get_images_google_place(event.location.place_id, "en")
        images += self.places_service.get_images_street_view(event.location_lat, event.location_lng)

        images = [{'idx': idx, 'url': image} for idx, image in enumerate(images)]

        if "image_idx" in request.GET:
            event.image_url = images[int(request.GET['image_idx'])]['url']
            event.save()
            return redirect("list_events")

        return render(request, self.template_name,
                      {'images': images, 'form': ImageUploadForm()})

#   def post(self, request, event_id):
#        form = ImageUploadForm(request.POST, request.FILES)
#        if form.is_valid():
#            f = request.FILES['file']
#            with open("media/{}.jpg".format(uuid.uuid4().hex), 'wb+') as destination:
#                for chunk in f.chunks():
#                    destination.write(chunk)
#            return redirect("list_events")
#        else:
#            messages.error(request, 'Invalid file, try again')

    @staticmethod
    def get_event_or_404(event_id, user_id):
        event = Event.objects.filter(pk=event_id, hosted_by=user_id).first()
        if not event:
            raise Http404()
        return event