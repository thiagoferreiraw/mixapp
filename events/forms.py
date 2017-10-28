from django.forms import ModelForm,  HiddenInput, Textarea, CharField, TextInput
from events.models import Category, Event, City


class EventForm(ModelForm):
    autocomplete_city = CharField(required=False, widget=TextInput(attrs={'id': 'autocomplete_city'}))
    autocomplete_location = CharField(required=False, widget=TextInput(attrs={'id': 'autocomplete_location'}))
    city_place_id = CharField(required=False, widget=HiddenInput(attrs={'id': 'city_place_id'}))
    location_place_id = CharField(required=False, widget=HiddenInput(attrs={'id': 'location_place_id'}))

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['hosted_by'].widget = HiddenInput()
        self.fields['city'].widget = HiddenInput()
        self.fields['location'].widget = HiddenInput()
        self.fields['category'].empty_label = "Select a category"
        self.fields['description'].widget = Textarea(attrs={'class': 'materialize-textarea'})
        self.fields['duration'].widget.attrs['min'] = 1
        self.fields['duration'].widget.attrs['max'] = 8
        self.fields['date'].widget.attrs['class'] = "datepicker"
        self.fields['time'].widget.attrs['class'] = "timepicker"

        if self.instance.pk:
            self.fields['autocomplete_city'].initial = self.instance.city.description
            self.fields['autocomplete_location'].initial = self.instance.location.description
            self.fields['city_place_id'].initial = self.instance.city.place_id
            self.fields['location_place_id'].initial = self.instance.location.place_id

    class Meta:
        model = Event
        fields = ('name', 'description', 'duration',
                  'date', 'time', 'city', 'category',
                  'location', 'expected_costs', 'hosted_by')