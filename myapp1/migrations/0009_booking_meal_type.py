# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0008_booking_pax_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='meal_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]