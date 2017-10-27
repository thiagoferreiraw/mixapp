from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'', include('pages.urls')),
    url(r'', include('users.urls')),
    url(r'', include('events.urls')),
    url(r'^admin/', admin.site.urls),
]
