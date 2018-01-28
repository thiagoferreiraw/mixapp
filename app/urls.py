from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from machina.app import board

urlpatterns = [
                  url(r'', include('pages.urls')),
                  url(r'', include('users.urls')),
                  url(r'', include('events.urls')),
                  url(r'^admin/', admin.site.urls),
                  url(r'^forum/', include(board.urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
