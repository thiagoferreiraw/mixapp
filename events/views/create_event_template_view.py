from django.shortcuts import render, redirect
from django.contrib import messages
from events.forms import EventTemplateForm
from django.views.generic import View


class EventTemplateCreateView(View):
    template_name = "events/event_template_form.html"
    form_action = "Create"

    def get(self, request):
        form = EventTemplateForm()
        return render(request, self.template_name,
                      {'form': form, 'user': request.user, 'form_action': self.form_action})

    def post(self, request):
        form = EventTemplateForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, 'Event Template created successfully')
            return redirect("list_event_template")

        return render(request, self.template_name,
                      {'form': form,  'user': request.user, 'form_action': self.form_action})

