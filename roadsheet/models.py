# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# График выезда
class DriverWorkload(models.Model):
    workload = models.CharField(max_length=100, editable=True,default = 0)
    def __unicode__(self):
        return str(self.workload)

# Водители
class Drivers(models.Model):
    first_name = models.CharField(max_length=100, editable = True)
    middle_name = models.CharField(max_length=100, editable = True)
    last_name = models.CharField(max_length=100, blank=True, editable=True)
    callsign = models.CharField(max_length=100,blank=True, editable = True)
    def __unicode__(self):
        return self.first_name + " " + self.middle_name[:1]+ " " + self.last_name[:1]

# Производители авто
class CarManufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=100, editable=True,default = 0)
    def __unicode__(self):
        return str(self.manufacturer_name)

# Модели авто
class CarModel(models.Model):
    manufacturer = models.ForeignKey(CarManufacturer,default = 0)
    model_name = models.CharField(max_length=100, editable = True, default = 0)
    def __unicode__(self):
        return str(str(self.manufacturer) + str(' ') + str(self.model_name))


class Cars(models.Model):
    board_number = models.CharField(max_length=4, editable = True)
    reg_number = models.CharField(max_length=10, editable = True)
    car_model = models.ForeignKey(CarModel, blank=True,default = 0, editable = True)
    def __unicode__(self):
        return self.reg_number.encode('utf8')

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
    tablet = models.ForeignKey(Tablets, default = 0)
    active = models.BooleanField(default=False, editable = False)
    workload = models.ForeignKey(DriverWorkload, default = 0)
    draft = models.NullBooleanField(default=True, editable = False)
    operator =  models.CharField(max_length=100, editable = False)
    car_state = models.BooleanField(default=True)
    car_fullgas = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.id)

