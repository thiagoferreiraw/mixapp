from django.shortcuts import render
from django.views.generic import View


class EventRequestConfirmationView(View):
    template_name = "events/event_request_confirmation.html"

    @staticmethod
    def get(request):
        return render(request,
                      "events/event_request_confirmation.html",
                      {'user': request.user})
