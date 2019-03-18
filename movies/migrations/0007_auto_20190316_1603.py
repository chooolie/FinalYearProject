# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-16 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_userdemographics_userratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userratings',
            name='rating',
            field=models.IntegerField(default=2, verbose_name='rating'),
        ),
        migrations.AlterField(
            model_name='userratings',
            name='tmdbId',
            field=models.IntegerField(default=1, verbose_name='TmdbId'),
        ),
    ]
