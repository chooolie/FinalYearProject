# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-04-05 01:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0042_groupmovielist_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmovielist',
            name='vote',
        ),
        migrations.AddField(
            model_name='groupmovielist',
            name='vote_dislikes',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
        migrations.AddField(
            model_name='groupmovielist',
            name='vote_likes',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
    ]
