from django.conf.urls import url, include
from events.views.create_event_view import EventCreateView
from events.views.edit_event_view import EventEditView
from events.views.list_event_view import EventListView
from events.views.search_event_view import EventSearchView
from events.views.choose_image_view import ChooseImageView
from events.views.event_details_view import EventDetailsView
from events.views.create_event_template_view import EventTemplateCreateView
from events.views.edit_event_template_view import EventTemplateEditView
from events.views.list_event_template_view import EventTemplateListView
from events.views.create_event_request_view import EventRequestView
from events.views.create_event_request_confirmation import EventRequestConfirmationView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^events/new/$',  login_required(EventCreateView.as_view()), name='create_event'),
    url(r'^events/edit/(?P<event_id>[0-9]+)$',  login_required(EventEditView.as_view()), name='edit_event'),
    url(r'^events/edit/(?P<event_id>[0-9]+)/image/$',  login_required(csrf_exempt(ChooseImageView.as_view())), name='edit_event_image'),
    url(r'^events/list/$',  login_required(EventListView.as_view()), name='list_events'),
    url(r'^events/search/$',  login_required(EventSearchView.as_view()), name='search_events'),
    url(r'^events/details/(?P<event_id>[0-9]+)$',  login_required(EventDetailsView.as_view()), name='event_details'),
    url(r'^events/templates/new/$',  login_required(EventTemplateCreateView.as_view()), name='create_event_template'),
    url(r'^events/templates/edit/(?P<template_id>[0-9]+)/$',  login_required(EventTemplateEditView.as_view()), name='edit_event_template'),
    url(r'^events/templates/list/$',  login_required(EventTemplateListView.as_view()), name='list_event_template'),
    url(r'^events/request/$',  login_required(EventRequestView.as_view()), name='request_event'),
    url(r'^events/request/confirmation$',  login_required(EventRequestConfirmationView.as_view()), name='request_event_confirmation'),
]
