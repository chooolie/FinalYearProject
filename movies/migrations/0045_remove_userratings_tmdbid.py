# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-04-07 23:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0044_auto_20190405_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userratings',
            name='tmdbId',
        ),
    ]
