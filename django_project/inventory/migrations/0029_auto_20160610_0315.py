# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-10 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0028_item__expiration_notified'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='_email_expiration',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='_email_old',
            field=models.BooleanField(default=False),
        ),
    ]
