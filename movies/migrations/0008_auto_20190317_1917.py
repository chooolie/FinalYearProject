# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-17 19:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20190316_1603'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userratings',
            old_name='movieId',
            new_name='movie_id_id',
        ),
        migrations.RenameField(
            model_name='userratings',
            old_name='userId',
            new_name='userId_id',
        ),
    ]