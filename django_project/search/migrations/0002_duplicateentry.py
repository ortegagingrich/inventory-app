# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-28 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicateEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wordkey', models.CharField(max_length=35)),
                ('defval', models.CharField(max_length=600)),
            ],
        ),
    ]