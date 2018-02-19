# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Profile(models.Model):
    ROLES_CHOICES = (
        ('operator', 'Оператор'),
        ('serviceman', 'Сервисный инженер'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLES_CHOICES)
    def __unicode__(self):
        return "Username: " + self.user.username + ". Role: "  + self.role


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Organization(models.Model):
    name = models.CharField(max_length=100, editable = True)
    inn = models.CharField(max_length=100, editable = True)
    address = models.CharField(max_length=100, editable = True)
    telephone = models.CharField(max_length=100, editable = True)
    service_address = models.CharField(max_length=100, editable = True)
    technical_chief = models.CharField(max_length=100, editable = True)
    mechanic_name = models.CharField(max_length=100, editable = True)
    def __unicode__(self):
        return str(self.name)


# График выезда - OK
class DriverWorkload(models.Model):
    workload = models.CharField(max_length=100, editable=True,default = 0)
    def __unicode__(self):
        return str(self.workload)

class DrLicenseCategory(models.Model):
    name = models.CharField(max_length=2, editable=True,default = 0)
    def __unicode__(self):
        return str(self.name)

# Водители - OK
class Drivers(models.Model):
    first_name = models.CharField(max_length=100, editable = True)
    middle_name = models.CharField(max_length=100, editable = True)
    last_name = models.CharField(max_length=100, blank=True, editable=True)
    callsign = models.CharField(max_length=100,blank=True, editable = True)
    license_number = models.CharField(max_length=100, editable=True, default=0)
    license_date = models.CharField(max_length=100, editable=True, default=0)
    license_category = models.ManyToManyField(DrLicenseCategory)

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

# Sim Operators
class SimOperators(models.Model):
    operator = models.CharField(max_length=50, blank=True, editable=True)
    def __unicode__(self):
        return self.operator.encode('utf8')


# SIM - ОК
class SimCards(models.Model):
    number = models.CharField(max_length=20, blank=True, editable=True)
    sn = models.CharField(max_length=50, blank=True, editable=True)
    operator = models.ForeignKey(SimOperators)
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
    def get_doc_quality_tablet(self):
        try:
            tmp = DocQualityTablet.objects.get(tablet=self)
        except Exception:
            tmp = None
        return tmp



# Путевые листы
class Roadsheets(models.Model):
    creation_timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    execution_timestamp = models.DateTimeField(blank=True, editable=False, null=True)
    closed_timestamp = models.DateTimeField(blank=True, editable=False, null=True)
    driver = models.ForeignKey(Drivers)
    car = models.ForeignKey(Cars)
    workload = models.ForeignKey(DriverWorkload)
    operator_open = models.CharField(max_length=100, editable = False)
    operator_close = models.CharField(max_length=100, editable = False)
    deleted = models.BooleanField(default=False, editable = False)
    def __unicode__(self):
        return str(self.id)

    def get_tablet(self):
        try:
            tmp = DocAddTmc.objects.filter(roadsheet=self).order_by('aparted_timestamp')[0]
        except Exception:
            tmp = None
        return tmp



class DocTabletSim(models.Model):
    tablet = models.ForeignKey(Tablets)
    sim = models.ForeignKey(SimCards)
    parted_timestamp = models.DateTimeField(auto_now_add=True, editable = True)
    aparted_timestamp = models.DateTimeField(blank=True, editable = False, null=True)
    def __unicode__(self):
        return str(str(self.tablet) + str(' - ') + str(self.sim))


class DocQualityTablet(models.Model):
    tablet = models.ForeignKey(Tablets)
    quality = models.ManyToManyField(TabletQuality)
    timestamp = models.DateTimeField(auto_now_add=True, editable=True)
    def __unicode__(self):
        return str(str(self.tablet) + str(' - ') + str(self.quality))
    def get_quality(self):
        try:
            tmp = TabletQuality.objects.filter(tablet=self)
        except Exception:
            tmp = None
        return tmp


class DocAddTmc(models.Model):
    tablet = models.ForeignKey(Tablets, null=True)
    roadsheet = models.ForeignKey(Roadsheets, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=True, null=True)
    aparted_timestamp = models.DateTimeField(blank=True, editable=False, null=True)



class DocRequest(models.Model):
    tablet = models.ForeignKey(Tablets, null=True)
    tablet_break_request =  models.ManyToManyField(TabletQuality)
    roadsheet = models.ForeignKey(Roadsheets, null=True, blank=True)
    comment = models.CharField(max_length=10000, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=True, null=True)
    timestamp_in_service = models.DateTimeField(blank=True, editable=False, null=True)
    closed_timestamp = models.DateTimeField(blank=True, editable=False, null=True)
    author = models.CharField(max_length=100, editable=False, null=True, blank=True)

    def __unicode__(self):
        return str(self.tablet)

class DocEndDay(models.Model):
    t_in_use = models.ManyToManyField(Tablets)
    t_accessible = models.ManyToManyField(Tablets, related_name="tab_access")
    t_in_diagnostic = models.ManyToManyField(Tablets, related_name="tab_diagnostic")
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    timestamp_approved = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    operator = models.CharField(max_length=100, editable=False, null=True, blank=True)
    operator_approved = models.CharField(max_length=100, editable=False, null=True, blank=True)

    def __unicode__(self):
        return str(self.id)
