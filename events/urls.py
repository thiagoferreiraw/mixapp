from django.conf.urls import url, include
from events.views.create_event_view import EventCreateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^events/new/$',  login_required(EventCreateView.as_view()), name='create_event'),
]
