# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-19 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0031_auto_20180219_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('operator', '\u041e\u043f\u0435\u0440\u0430\u0442\u043e\u0440'), ('serviceman', '\u0421\u0435\u0440\u0432\u0438\u0441\u043d\u044b\u0439 \u0438\u043d\u0436\u0435\u043d\u0435\u0440')], max_length=100),
        ),
    ]
