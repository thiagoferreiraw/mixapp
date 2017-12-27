from django.shortcuts import render, redirect
from django.views.generic import View
from events.models import EventTemplate


class EventTemplateListView(View):
    template_name = "events/list_event_template.html"

    def get(self, request):
        templates = EventTemplate.objects.filter().order_by("name")
        return render(request, self.template_name, {'templates': templates})

