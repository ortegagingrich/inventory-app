# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20160321_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='opened_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='printed_expiration_date',
            field=models.DateField(blank=True),
        ),
    ]
