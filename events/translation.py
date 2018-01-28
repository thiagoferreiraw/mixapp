from modeltranslation.translator import translator, TranslationOptions
from events.models import Category, EventTemplate

class CategoryTranslationOptions(TranslationOptions):
    fields = ('description', 'name',)

class EventTemplateTranslationOptions(TranslationOptions):
    fields = ('description', 'name',)

translator.register(Category, CategoryTranslationOptions)
translator.register(EventTemplate, EventTemplateTranslationOptions)