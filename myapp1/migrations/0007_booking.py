# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 11:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp1', '0006_delete_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provision_code', models.CharField(max_length=255)),
                ('hotel_code', models.CharField(max_length=255)),
                ('booking_code', models.CharField(max_length=255)),
                ('coral_booking_code', models.CharField(max_length=255)),
                ('room_type', models.CharField(max_length=255)),
                ('room_description', models.CharField(max_length=255)),
                ('room_category', models.CharField(max_length=255)),
                ('pax_names', models.TextField(max_length=255)),
                ('status', models.CharField(max_length=100)),
                ('list_price', models.FloatField(default=0.0)),
                ('currency', models.CharField(max_length=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]