# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-18 12:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0015_auto_20190318_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userratings',
            name='userdemo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.UserDemographics'),
        ),
    ]
