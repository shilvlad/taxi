# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-31 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roadsheet', '0010_docrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='docrequest',
            name='author',
            field=models.CharField(default=0, editable=False, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='docrequest',
            name='closed_timestamp',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='docrequest',
            name='comment',
            field=models.CharField(max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='docrequest',
            name='tablet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='roadsheet.Tablets'),
        ),
        migrations.AddField(
            model_name='docrequest',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]