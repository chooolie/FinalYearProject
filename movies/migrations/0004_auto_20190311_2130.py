# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-11 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20190311_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topmovies',
            name='genre',
            field=models.CharField(default='', max_length=300, verbose_name='genres'),
        ),
    ]