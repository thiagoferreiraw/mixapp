from django.contrib.auth.forms import UserCreationForm as UserCreationFormDjango, User, UsernameField
from django.forms import ModelForm, MultipleChoiceField
from users.models import Category, UserCategory
from django.conf import settings


class UserCreationForm(UserCreationFormDjango):

    def __init__(self, *args, **kwargs):
        super(UserCreationFormDjango, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': '', 'required':True})
        self.fields['last_name'].widget.attrs.update({'required': True})
        self.fields['email'].widget.attrs.update({'required': True})


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email","id")
        field_classes = {'username': UsernameField}

    def save(self, commit=True, chosen_categories=[], signup_invitation=None):
        user = super(UserCreationForm, self).save(commit=True)

        signup_invitation.user_has_signed_up = True
        signup_invitation.save()

        for category in chosen_categories:
            user_category = UserCategory(user_id_id=user.id, category_id_id=category)
            user_category.save()

        return user


class UserEditProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': '', 'required':True})
        self.fields['last_name'].widget.attrs.update({'required': True})
        self.fields['email'].widget.attrs.update({'required': True})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def save(self, commit=True, chosen_categories=[]):
        user = super(UserEditProfileForm, self).save(commit=True)

        UserCategory.objects.filter(user_id=user).delete()
        for category in chosen_categories:
            user_category = UserCategory(user_id_id=user.id, category_id_id=category)
            user_category.save()

        return user
