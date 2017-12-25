# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-25 19:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0014_roadsheets_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadsheets',
            name='closed_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='roadsheets',
            name='deleted',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]