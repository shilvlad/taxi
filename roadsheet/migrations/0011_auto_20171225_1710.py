# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-25 14:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0010_auto_20171225_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarStates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(default=0, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='roadsheets',
            name='workload',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='roadsheet.DriverWorkload'),
        ),
        migrations.AddField(
            model_name='cars',
            name='car_state',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='roadsheet.CarStates'),
        ),
    ]
