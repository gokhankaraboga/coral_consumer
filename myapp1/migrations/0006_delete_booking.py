# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 11:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0005_auto_20161108_1316'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Booking',
        ),
    ]