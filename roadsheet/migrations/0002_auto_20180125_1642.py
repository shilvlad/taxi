# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-25 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctabletsim',
            name='aparted_timestamp',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
