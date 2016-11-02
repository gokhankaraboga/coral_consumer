from __future__ import unicode_literals

from django.db import models



# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __unicode__(self):
        return 'Object: ' + str(self.pk)


class Manager(models.Model):
    manager_name = models.CharField(max_length=75)
    position = models.IntegerField()
