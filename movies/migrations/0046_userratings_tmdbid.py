# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-04-08 13:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0045_remove_userratings_tmdbid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userratings',
            name='tmdbId',
            field=models.IntegerField(default=1, verbose_name='TmdbId'),
        ),
    ]
