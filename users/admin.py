from django.contrib import admin

from users.models import Category, SignupInvitation


class CategoryAdmin(admin.ModelAdmin):
    pass

class SignupInvitationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(SignupInvitation, SignupInvitationAdmin)

