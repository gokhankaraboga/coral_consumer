from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Destination(models.Model):
    coral_code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)


class Booking(models.Model):
    pass


class Hotel(models.Model):
    coral_code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
