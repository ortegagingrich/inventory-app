# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0027_itemtype_initialized'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='_expiration_notified',
            field=models.BooleanField(default=False),
        ),
    ]
