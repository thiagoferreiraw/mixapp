from django.forms import ModelForm,  HiddenInput
from events.models import Category, Event, City
from events.services import PlacesService

class EventCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['hosted_by'].widget = HiddenInput()
        self.fields['hosted_by'].required = False
        self.fields['city'].widget = HiddenInput()
        self.fields['city'].required = False
        self.fields['category'].required = False

    class Meta:
        model = Event
        fields = ('name', 'description', 'duration', 'date', 'time', 'city', 'category', 'location', 'expected_costs', 'hosted_by')

    def save(self, commit=True, user_id=None, google_city_id=None):
        event = super(EventCreateForm, self).save()

        event.hosted_by_id = user_id

        event.city = PlacesService().get_and_save_city(google_city_id, "en")

        event.save()

        return event


