from django.conf.urls import url, include
from events.views.create_event_view import EventCreateView
from events.views.list_event_view import EventListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^events/new/$',  login_required(EventCreateView.as_view()), name='create_event'),
    url(r'^events/list/$',  login_required(EventListView.as_view()), name='list_events'),
]
