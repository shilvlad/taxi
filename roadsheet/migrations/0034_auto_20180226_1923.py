# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-26 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0033_auto_20180226_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docaddtmc',
            name='cable_without_charger',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='docaddtmc',
            name='charger_with_cable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='docaddtmc',
            name='charger_without_cable',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='docaddtmc',
            name='craddle',
            field=models.BooleanField(default=False),
        ),
    ]