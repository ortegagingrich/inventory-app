# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_locationdefault'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='default',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='inventory.LocationDefault'),
        ),
    ]
