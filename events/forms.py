from django.forms import ModelForm,  HiddenInput, Textarea
from events.models import Category, Event, City
from events.services import PlacesService

class EventCreateForm(ModelForm):

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

    class Meta:
        model = Event
        fields = ('name', 'description', 'duration', 'date', 'time', 'city', 'category', 'location', 'expected_costs', 'hosted_by')


