# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-25 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0013_auto_20171225_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadsheets',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]