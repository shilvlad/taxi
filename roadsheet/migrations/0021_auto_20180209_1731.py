# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-09 14:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0020_auto_20180209_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimOperators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='simcards',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roadsheet.SimOperators'),
        ),
    ]
