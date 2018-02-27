from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from .models import Roadsheets, Drivers, Tablets, Cars, CarManufacturer, CarModel, DriverWorkload, \
    TabletQuality, DocTabletSim, SimCards, DocAddTmc, DocQualityTablet, DocRequest, SimOperators, DocEndDay, \
    Organization, DrLicenseCategory, Profile, Insurance, TO

admin.site.register(Drivers)
admin.site.register(Roadsheets)
admin.site.register(Tablets)
admin.site.register(Cars)
admin.site.register(CarModel)
admin.site.register(CarManufacturer)
admin.site.register(DriverWorkload)
admin.site.register(TabletQuality)
admin.site.register(SimCards)
admin.site.register(DocTabletSim)
admin.site.register(DocAddTmc)
admin.site.register(DocQualityTablet)
admin.site.register(SimOperators)
admin.site.register(DocRequest)
admin.site.register(DocEndDay)
admin.site.register(Organization)
admin.site.register(DrLicenseCategory)
admin.site.register(Profile)
admin.site.register(Insurance)
admin.site.register(TO)