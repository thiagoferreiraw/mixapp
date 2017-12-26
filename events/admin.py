from django.contrib import admin

from events.models import City, Category, Event, Location, Language, EventTemplate, Palindrome




class CategoryAdmin(admin.ModelAdmin):
    pass


class CityAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass


class LanguageAdmin(admin.ModelAdmin):
    pass

class TemplateAdmin(admin.ModelAdmin):
    pass

class PalindromeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(EventTemplate, TemplateAdmin)
admin.site.register(Palindrome, PalindromeAdmin)


