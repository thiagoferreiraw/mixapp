from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from users import views as user_views


urlpatterns = [
    url(r'^home/$', user_views.home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/(?P<invitation_hash>\w{1,50})/$', user_views.signup, name='signup'),
    url(r'^user/profile/$', user_views.edit_profile, name='edit_profile'),
    url(r'^user/settings/$', user_views.settings, name='settings'),
    url(r'^user/settings/password/$', user_views.password, name='password'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]
