from django import forms
from django.forms import Form, ModelForm,  HiddenInput, Textarea, CharField, TextInput, FileField
from events.models import Category, Event, City
from datetime import datetime


class EventForm(ModelForm):
    autocomplete_city = CharField(required=False, widget=TextInput(attrs={'id': 'autocomplete_city'}))
    autocomplete_location = CharField(required=False, widget=TextInput(attrs={'id': 'autocomplete_location'}))
    city_place_id = CharField(required=False, widget=HiddenInput(attrs={'id': 'city_place_id'}))
    location_place_id = CharField(required=False, widget=HiddenInput(attrs={'id': 'location_place_id'}))

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        self.set_up_widgets()

        if self.instance.pk:
            self.fields['autocomplete_city'].initial = self.instance.city.description
            self.fields['autocomplete_location'].initial = self.instance.location.description
            self.fields['city_place_id'].initial = self.instance.city.place_id
            self.fields['location_place_id'].initial = self.instance.location.place_id

    def is_valid(self):
        valid = super(EventForm,self).is_valid()
        if not valid:
            return valid

        if self.cleaned_data['date'] < datetime.now().date():
            self.add_error("date", "Invalid date. Date must be equal or greater than {}".format(str(self.cleaned_data['date'])))
            return False

        date_time_form = datetime.combine(self.cleaned_data['date'], self.cleaned_data['time'])
        if date_time_form < datetime.now():
            self.add_error("time",
                           "Invalid time. Date and time must be equal or greater than {}".format(str(datetime.now())[:16]))
            return False

        return True

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'duration',
                  'date', 'time', 'city', 'category',
                  'location', 'expected_costs', 'hosted_by',
                  'location_lat', 'location_lng')

    def set_up_widgets(self):
        self.fields['category'].empty_label = "Select a category"
        self.fields['description'].widget = Textarea(attrs={'class': 'materialize-textarea'})
        self.fields['duration'].widget.attrs.update({'min': 1, 'max': 10})
        self.fields['expected_costs'].widget.attrs.update({'min': 0})
        self.fields['date'].widget.attrs['class'] = "datepicker"
        self.fields['time'].widget.attrs['class'] = "timepicker"
        self.fields['location_lat'].widget = HiddenInput(attrs={'id': 'location_lat'})
        self.fields['location_lng'].widget = HiddenInput(attrs={'id': 'location_lng'})


class ImageUploadForm(Form):
    file = FileField()


class SearchForm(Form):

    categories = Category.objects.all()
    CATEGORIES_CHOICES = [('', 'Select a category')]
    for c in categories:
        CATEGORIES_CHOICES.append((c.id, c.name))

    cities = City.objects.raw("select city.id, city.description || ' ('|| (select count(1) from events_event where city_id = city.id  and datetime > current_timestamp ) || ')' as description from events_city city")
    CITIES_CHOICES = [('', 'Select a city')]
    for c in cities:
        CITIES_CHOICES.append((c.id, c.description))

    category = forms.ChoiceField(choices=(CATEGORIES_CHOICES), required=False, label=False)
    city = forms.ChoiceField(choices=(CITIES_CHOICES), required=False, label=False)
