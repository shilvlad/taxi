# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-31 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0009_auto_20180131_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
