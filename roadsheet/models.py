# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# График выезда - OK
class DriverWorkload(models.Model):
    workload = models.CharField(max_length=100, editable=True,default = 0)
    def __unicode__(self):
        return str(self.workload)

# Водители - OK
class Drivers(models.Model):
    first_name = models.CharField(max_length=100, editable = True)
    middle_name = models.CharField(max_length=100, editable = True)
    last_name = models.CharField(max_length=100, blank=True, editable=True)
    callsign = models.CharField(max_length=100,blank=True, editable = True)
    def __unicode__(self):
        return self.first_name + " " + self.middle_name[:1]+ " " + self.last_name[:1]

# Производители авто  - OK
class CarManufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=100, editable=True,default = 0)
    def __unicode__(self):
        return str(self.manufacturer_name)

# Модели авто  - OK
class CarModel(models.Model):
    manufacturer = models.ForeignKey(CarManufacturer,default = 0)
    model_name = models.CharField(max_length=100, editable = True, default = 0)
    def __unicode__(self):
        return str(str(self.manufacturer) + str(' ') + str(self.model_name))

# Автомобили - OK
class Cars(models.Model):
    board_number = models.CharField(max_length=4, editable = True)
    reg_number = models.CharField(max_length=10, editable = True)
    car_model = models.ForeignKey(CarModel, blank=True,default = 0, editable = True)
    def __unicode__(self):
        return self.board_number.encode('utf8')



# Статусы - ОК
class TabletQuality(models.Model):
    status = models.CharField(max_length=100, editable = True)
    def __unicode__(self):
        return self.status.encode('utf8')

# SIM - ОК
class SimCards(models.Model):
    number = models.CharField(max_length=20, blank=True, editable=True)
    sn = models.CharField(max_length=50, blank=True, editable=True)
    operator = models.CharField(max_length=50, blank=True, editable=True)
    in_use = models.BooleanField(default=True)
    def __unicode__(self):
        return str(self.number)

# Планшеты - ОК
class Tablets(models.Model):
    model = models.CharField(max_length=100,blank=True, editable = True)
    serial_number = models.CharField(max_length=100,blank=True, editable = True)
    internal_code = models.CharField(max_length=100,blank=True, editable = True)
    def __unicode__(self):
        return str(self.internal_code)

# Путевые листы
class Roadsheets(models.Model):
    creation_timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    execution_timestamp = models.DateTimeField(blank=True, editable=False, null=True)
    closed_timestamp = models.DateTimeField(blank=True, editable=False, null=True)
    driver = models.ForeignKey(Drivers)
    car = models.ForeignKey(Cars)
    workload = models.ForeignKey(DriverWorkload)
    operator =  models.CharField(max_length=100, editable = False)
    deleted = models.BooleanField(default=False, editable = False)
    def __unicode__(self):
        return str(self.id)

class DocTabletSim(models.Model):
    tablet = models.ForeignKey(Tablets)
    sim = models.ForeignKey(SimCards)
    parted_timestamp = models.DateTimeField(auto_now_add=True, editable = True)
    aparted_timestamp = models.DateTimeField(blank=True, editable = False, null=True)
    def __unicode__(self):
        return str(str(self.tablet) + str(' - ') + str(self.sim))


class DocQualityTablet(models.Model):
    tablet = models.ForeignKey(Tablets)
    quality = models.ForeignKey(TabletQuality)
    timestamp = models.DateTimeField(auto_now_add=True, editable=True)


class DocAddTmc(models.Model):
    tablet = models.ForeignKey(Tablets, null=True)
    roadsheet = models.ForeignKey(Roadsheets, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=True, null=True)
    aparted_timestamp = models.DateTimeField(blank=True, editable=False, null=True)
    def __unicode__(self):
        return str(self.tablet)
