from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Drivers(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100,blank=True, editable = True)
    last_name = models.CharField(max_length=100, blank=True, editable=True)
    def __unicode__(self):
        return self.first_name + " " + self.middle_name[:1]+ " " + self.last_name[:1]

class Cars(models.Model):

    def __unicode__(self):
        return str(self.id)

class Tablets(models.Model):
    model = models.CharField(max_length=100,blank=True, editable = True)
    serial_number = models.CharField(max_length=100,blank=True, editable = True)
    internal_code = models.CharField(max_length=100,blank=True, editable = True)
    def __unicode__(self):
        return str(self.id)

class Roadsheets(models.Model):
    execution_datetime = models.DateTimeField(auto_now_add=True ,blank=True, editable = True)
    driver = models.ForeignKey(Drivers)
    car = models.ForeignKey(Cars, blank=True,default = 0)
    tablet = models.ForeignKey(Tablets, blank=True,default = 0)
    previous_record = models.ForeignKey('self', null = True, default=0, editable = True)
    active = models.BooleanField(default=True)
    def __unicode__(self):
        return str(self.id)

