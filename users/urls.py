from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from users.views import views as user_views
from users.views.moderator_flow.moderator_setup_view import ModeratorSetupView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^home/$', user_views.home, name='home'),
    url(r'^login/$', user_views.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^waiting_list/$', user_views.UserWaitingListView.as_view(), name='waiting_list'),
    url(r'^user/send_invitation/$', user_views.UserInvitationView.as_view(), name='send_invitation'),
    url(r'^signup/(?P<invitation_hash>\w[a-zA-Z0-9-_]{1,50})/$', user_views.UserSignupView.as_view(), name='signup'),
    url(r'^user/profile/$',  login_required(user_views.UserEditProfileView.as_view()), name='edit_profile'),
    url(r'^user/settings/$', user_views.settings, name='settings'),
    url(r'^user/moderator_setup/$', ModeratorSetupView.as_view(), name='moderator_setup'),
    url(r'^user/settings/password/$', user_views.password, name='password'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    # Password reset
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]
