from django.shortcuts import render, redirect
from django.views.generic import View
from events.models import Event


class EventListView(View):
    template_name = "events/list_events.html"

    def get(self, request):
        events = Event.objects.filter(hosted_by_id=request.user.id)
        return render(request, self.template_name, {'event_list': events})

