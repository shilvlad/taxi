# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-01 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0015_auto_20180201_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docrequest',
            name='roadsheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='roadsheet.Roadsheets'),
        ),
    ]