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


class UserEditProfileForm(UserCreationFormDjango):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormDjango, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': '', 'required': True})
        self.fields['last_name'].widget.attrs.update({'required': True})
        self.fields['email'].widget.attrs.update({'required': True})

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",)

    # def save(self, commit=True):
    #     user = User.objects.get()
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user