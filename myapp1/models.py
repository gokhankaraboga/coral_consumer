from __future__ import unicode_literals

from django.db import models
import django.contrib.auth.models as auth_models


# Create your models here.
class Destination(models.Model):
    coral_code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Destination: ' + self.coral_code


class Booking(models.Model):
    user_id = models.ForeignKey(auth_models.User)
    provision_code = models.CharField(max_length=255)
    hotel_name = models.CharField(max_length=255, null=True)
    hotel_code = models.CharField(max_length=255)
    checkin = models.CharField(max_length=255, null=True)
    checkout = models.CharField(max_length=255, null=True)
    booking_code = models.CharField(max_length=255)
    coral_booking_code = models.CharField(max_length=255)
    room_type = models.CharField(max_length=255)
    room_description = models.CharField(max_length=255)
    room_category = models.CharField(max_length=255)
    meal_type = models.CharField(max_length=100, null=True)
    pax_count = models.IntegerField(null=True)
    pax_names = models.TextField(max_length=255)
    status = models.CharField(max_length=100)
    list_price = models.FloatField(default=0.0)
    currency = models.CharField(max_length=10)

    def __unicode__(self):
        return 'Booking: ' + self.pax_names


class Hotel(models.Model):
    coral_code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return 'Hotel: ' + self.coral_code
