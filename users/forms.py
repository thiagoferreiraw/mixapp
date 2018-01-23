from django.contrib.auth.forms import UserCreationForm as UserCreationFormDjango, User, UsernameField
from django.forms import ModelForm, MultipleChoiceField, CharField, TextInput, HiddenInput
from users.models import Category, UserCategory, SignupInvitation, SignupWaitingList, Profile, UserLanguage, City
from django.conf import settings
from django.core import validators
from datetime import datetime


class UserCreationForm(UserCreationFormDjango):

    def __init__(self, *args, **kwargs):
        super(UserCreationFormDjango, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].widget.attrs.update({'autofocus': ''})

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "id")
        field_classes = {'username': UsernameField}

    def is_valid(self):
        valid = super(UserCreationForm, self).is_valid()

        if not valid:
            return valid

        email_exists = len(User.objects.filter(email=self.cleaned_data['email'])) > 0
        if email_exists:
            self.add_error("email", "This email is already in use")
            return False

        return True

    def save(self, commit=True, chosen_categories=[], chosen_languages=[], signup_invitation=None):
        user = super(UserCreationForm, self).save(commit=True)

        signup_invitation.user_has_signed_up = True
        signup_invitation.save()

        for category in chosen_categories:
            user_category = UserCategory(user_id_id=user.id, category_id_id=category)
            user_category.save()

        for language in chosen_languages:
            user_language = UserLanguage(user_id_id=user.id, language_id_id=language)
            user_language.save()

        return user


class UserEditProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].widget.attrs.update({'autofocus': '', 'required':True})

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def save(self, commit=True, chosen_categories=[], chosen_languages=[]):
        user = super(UserEditProfileForm, self).save(commit=True)

        UserCategory.objects.filter(user_id=user).delete()
        for category in chosen_categories:
            user_category = UserCategory(user_id_id=user.id, category_id_id=category)
            user_category.save()

        UserLanguage.objects.filter(user_id=user).delete()
        for language in chosen_languages:
            user_language = UserLanguage(user_id_id=user.id, language_id_id=language)
            user_language.save()

        return user


class UserInvitationForm(ModelForm):
    class Meta:
        model = SignupInvitation
        fields = ('email_invited',)


class UserWaitingListForm(ModelForm):
    class Meta:
        model = SignupWaitingList
        fields = ('email',)


class ProfileForm(ModelForm):
    autocomplete_birth_city = CharField(required=False, widget=TextInput(attrs={'id': 'autocomplete_birth_city'}))
    birth_city_place_id = CharField(required=False, widget=HiddenInput(attrs={'id': 'birth_city_place_id'}))
    autocomplete_current_city = CharField(required=False, widget=TextInput(attrs={'id': 'autocomplete_current_city'}))
    current_city_place_id = CharField(required=False, widget=HiddenInput(attrs={'id': 'current_city_place_id'}))

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        self.set_up_widgets()

        if self.instance.birth_city:
            self.fields['autocomplete_birth_city'].initial = self.instance.birth_city.description
            self.fields['birth_city_place_id'].initial = self.instance.birth_city.place_id
            self.fields['autocomplete_current_city'].initial = self.instance.current_city.description
            self.fields['current_city_place_id'].initial = self.instance.current_city.place_id

    def is_valid(self):
        valid = super(ProfileForm,self).is_valid()
        if not valid:
            return valid

        if self.cleaned_data['birth_date'] >= datetime.now().date():
            self.add_error("birth_date", "Invalid birth date.")
            return False

        return True

    class Meta:
        model = Profile
        fields = ('birth_city', 'current_city', 'birth_date')

    def set_up_widgets(self):
        self.fields['birth_date'].widget.attrs['class'] = "datepicker"
        self.fields['birth_date'].required = True
