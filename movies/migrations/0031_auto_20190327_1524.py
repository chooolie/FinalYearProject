# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-27 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0030_groupinfo_groupusers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinfo',
            name='group_name',
            field=models.CharField(max_length=50, unique=True, verbose_name='name'),
        ),
    ]
