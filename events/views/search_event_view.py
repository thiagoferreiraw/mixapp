from django.shortcuts import render, redirect
from django.views.generic import View
from events.models import Event, Category, City
from events.forms import SearchForm
from django.http import HttpResponse
from datetime import datetime


class EventSearchView(View):
    template_name = "events/search_events.html"

    def get(self, request):
        context = {'form': SearchForm(request.GET)}

        category = request.GET.get('category')
        city = request.GET.get('city')

        events = Event.objects.filter(date__gte=datetime.now().date())

        if category:
            events = events.filter(template__category__id=category)

        if city:
            events = events.filter(city__id=city)     
            
        context['events']=events
        
        return render(request, self.template_name, context)
