# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-30 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0003_auto_20180125_2000'),
    ]

    operations = [
       migrations.AddField(
            model_name='docqualitytablet',
            name='aparted_timestamp',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]