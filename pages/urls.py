from django.conf.urls import url, include
from pages import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index2/$', views.index2, name='indext2'),
    url(r'^find/$', views.find, name='find'),
    url(r'^feedback/$', views.feedback, name='feedback'),
]
