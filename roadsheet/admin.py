from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from .models import Roadsheets, Drivers, Tablets, Cars

admin.site.register(Drivers)
admin.site.register(Roadsheets)
admin.site.register(Tablets)
admin.site.register(Cars)