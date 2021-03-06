# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-25 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer_name', models.CharField(default=0, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(default=0, max_length=100)),
                ('manufacturer', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='roadsheet.CarManufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_number', models.CharField(max_length=4)),
                ('reg_number', models.CharField(max_length=10)),
                ('car_model', models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='roadsheet.CarModel')),
            ],
        ),
        migrations.CreateModel(
            name='DocQualityTablet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocTabletSim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parted_timestamp', models.DateTimeField(auto_now_add=True)),
                ('aparted_timestamp', models.DateTimeField(blank=True, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Drivers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('callsign', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DriverWorkload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workload', models.CharField(default=0, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Roadsheets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_datetime', models.DateTimeField(auto_now_add=True)),
                ('closed_datetime', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False, editable=False)),
                ('draft', models.NullBooleanField(default=True, editable=False)),
                ('operator', models.CharField(editable=False, max_length=100)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadsheet.Cars')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadsheet.Drivers')),
                ('workload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadsheet.DriverWorkload')),
            ],
        ),
        migrations.CreateModel(
            name='SimCards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=20)),
                ('sn', models.CharField(blank=True, max_length=50)),
                ('operator', models.CharField(blank=True, max_length=50)),
                ('in_use', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TabletQuality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tablets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(blank=True, max_length=100)),
                ('serial_number', models.CharField(blank=True, max_length=100)),
                ('internal_code', models.CharField(blank=True, max_length=100)),
            ],
        ),

        migrations.AddField(
            model_name='doctabletsim',
            name='sim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadsheet.SimCards'),
        ),
        migrations.AddField(
            model_name='doctabletsim',
            name='tablet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadsheet.Tablets'),
        ),
        migrations.AddField(
            model_name='docqualitytablet',
            name='quality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadsheet.TabletQuality'),
        ),
        migrations.AddField(
            model_name='docqualitytablet',
            name='tablet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadsheet.Tablets'),
        ),
    ]
