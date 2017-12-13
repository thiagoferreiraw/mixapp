from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from events.forms import EventTemplateForm, EventTemplate
from django.views.generic import View


class EventTemplateEditView(View):
    template_name = "events/event_template_form.html"
    form_action = "Create"

    def get(self, request, template_id):
        template = get_object_or_404(EventTemplate, pk=template_id)
        form = EventTemplateForm(instance=template)
        return render(request, self.template_name,
                      {'form': form, 'user': request.user, 'form_action': self.form_action})

    def post(self, request, template_id):
        template = get_object_or_404(EventTemplate, pk=template_id)
        form = EventTemplateForm(request.POST, instance=template)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event Template created successfully')
            return redirect("list_event_template")

        return render(request, self.template_name,
                      {'form': form,  'user': request.user, 'form_action': self.form_action})

