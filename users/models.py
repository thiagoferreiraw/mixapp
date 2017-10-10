from django.db import models
from django.contrib.auth.models import User


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
