from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Category, Language, City
import uuid


class UserCategory(models.Model):
    user_id = models.ForeignKey(User)
    category_id = models.ForeignKey(Category)

    class Meta:
        unique_together = (("user_id", "category_id"),)


class SignupInvitation(models.Model):
    email_invited = models.EmailField()
    invited_by = models.ForeignKey(User, null=True)
    user_has_signed_up = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, blank=True, editable=True)
    hash = models.UUIDField(default=uuid.uuid4, unique=True, editable=True)

    def __str__(self):
        return self.email_invited + " - " + str(self.hash)
        

class SignupWaitingList(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateField(auto_now_add=True, blank=True, editable=True)

    def __str__(self):
        return self.email


class UserLanguage(models.Model):
    user_id = models.ForeignKey(User)
    language_id = models.ForeignKey(Language)

    class Meta:
        unique_together = (("user_id", "language_id"),)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    birth_city = models.ForeignKey(City, related_name="birth_city", null=True)
    actual_city = models.ForeignKey(City, related_name="actual_city", null=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
