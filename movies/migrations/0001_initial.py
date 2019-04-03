# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-11 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=300, verbose_name='name')),
                ('genre', models.CharField(default='', max_length=300, verbose_name='genre')),
            ],
        ),
    ]
