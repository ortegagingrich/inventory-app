# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 11:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20160410_0405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='location_date',
            new_name='_location_date',
        ),
    ]
