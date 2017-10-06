from django.contrib.auth.forms import UserCreationForm as UserCreationFormDjango, User, UsernameField
from django.conf import settings


class UserCreationForm(UserCreationFormDjango):

    def __init__(self, *args, **kwargs):
        super(UserCreationFormDjango, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': '', 'required':True})
        self.fields['last_name'].widget.attrs.update({'required': True})
        self.fields['email'].widget.attrs.update({'required': True})


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)
        field_classes = {'username': UsernameField}


