from django.db import models
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


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


