from django.contrib import admin

from users.models import SignupInvitation

class SignupInvitationAdmin(admin.ModelAdmin):
    pass

admin.site.register(SignupInvitation, SignupInvitationAdmin)

