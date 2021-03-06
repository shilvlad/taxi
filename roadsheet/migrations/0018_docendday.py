# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-09 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0017_auto_20180201_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocEndDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('timestamp_approved', models.DateTimeField(auto_now_add=True, null=True)),
                ('operator', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('operator_approved', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('t_in_use', models.ManyToManyField(to='roadsheet.Tablets')),
            ],
        ),
    ]
