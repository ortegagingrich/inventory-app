# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationmodel',
            name='unread',
            field=models.BooleanField(default=True),
        ),
    ]
