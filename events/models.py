from django.db import models
from users.models import User
from datetime import datetime
from django.conf import settings
import urllib
import os
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from sorl.thumbnail import get_thumbnail
import uuid


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
    photo_reference = models.CharField(max_length=500, null=True)
    photo_url = models.CharField(max_length=500, null=True)
    timezone = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.description


class Location(models.Model):
    description = models.CharField(max_length=300)
    place_id = models.CharField(max_length=300, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    photo_reference = models.CharField(max_length=500, null=True)
    photo_url = models.CharField(max_length=500, null=True)
    timezone = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.description


class LocationImage(models.Model):
    url = models.CharField(max_length=500)
    location = models.ForeignKey(Location)


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    duration = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    datetime = models.DateTimeField()
    city = models.ForeignKey(City)
    location = models.ForeignKey(Location)
    location_lat = models.FloatField()
    location_lng = models.FloatField()
    expected_costs = models.FloatField()
    hosted_by = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    image_url = models.CharField(max_length=500, null=True)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name

    def get_remote_image(self):
        if self.image_url:
            print(self.image_url)
            result = urllib.request.urlretrieve(self.image_url)
            self.image.save(
                os.path.basename(uuid.uuid4().hex+".jpg"),
                File(open(result[0], 'rb'))
            )
            self.save()

    def save(self, *args, **kwargs):
        if self.date is not None and self.time is not None:
            self.datetime = datetime.combine(date=self.date, time=self.time)
        super(Event, self).save(*args, **kwargs)

