# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-27 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0039_auto_20180227_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablets',
            name='timestamp_foolished',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tablets',
            name='timestamp_lost',
            field=models.DateTimeField(null=True),
        ),
    ]