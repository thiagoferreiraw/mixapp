from django.shortcuts import render, redirect
from django.views.generic import View
from events.models import Event, Category, City
from django.http import HttpResponse


class EventSearchView(View):
    template_name = "events/search_events.html"

    categories = Category.objects.all()
    cities = City.objects.raw("select city.id, city.description || ' ('|| (select count(1) from events_event where city_id = city.id  and datetime > current_timestamp ) || ')' as description from events_city city")    
    context = {
        'categories': categories,
        'cities': cities
    }

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        
        category = request.POST['select-categories']
        city = request.POST['select-cities']

        events = Event.objects.all()
        if category:
            category = Category.objects.get(name=category)
            events = events.filter(category=category.id)

        if city:
            city = city[:-4]
            city = City.objects.get(description__contains=city)
            events = events.filter(city=city.id)            
            
        self.context['events']=events
        
        return render(request, self.template_name, self.context)