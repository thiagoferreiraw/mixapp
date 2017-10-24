from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class City(models.Model):
    description = models.CharField(max_length=300)
    place_id = models.CharField(max_length=300, unique=True)
    image = models.CharField(max_length=300, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timezone = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.description

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    duration = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    city = models.ForeignKey(City, null=True)
    location = models.CharField(max_length=300)
    expected_costs = models.FloatField()
    hosted_by = models.ForeignKey(User, null=True)
    category = models.ForeignKey(Category, null=True)

    def __str__(self):
        return self.name