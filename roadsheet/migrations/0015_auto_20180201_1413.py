# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-01 11:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0014_auto_20180201_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docrequest',
            name='author',
            field=models.CharField(blank=True, editable=False, max_length=100, null=True),
        ),
    ]
