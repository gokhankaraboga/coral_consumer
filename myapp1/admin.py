from django.contrib import admin

from . import models

admin.site.register(models.Destination)
admin.site.register(models.Hotel)
admin.site.register(models.Booking)
