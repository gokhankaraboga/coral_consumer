# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 13:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0003_booking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='destination_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='hotel',
            old_name='hotel_name',
            new_name='name',
        ),
    ]