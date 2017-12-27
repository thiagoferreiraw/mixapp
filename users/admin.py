from django.contrib import admin

from users.models import SignupInvitation, UserCategory

class SignupInvitationAdmin(admin.ModelAdmin):
    pass

class UserCategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(SignupInvitation, SignupInvitationAdmin)
admin.site.register(UserCategory, UserCategoryAdmin)

