# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('myapp1', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
