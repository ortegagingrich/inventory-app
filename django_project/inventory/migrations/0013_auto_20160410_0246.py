# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20160409_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemTypeDefault',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='location',
            name='name_default',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
