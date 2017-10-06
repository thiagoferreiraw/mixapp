from django.conf.urls import url, include
from pages import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
