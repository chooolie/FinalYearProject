# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-27 20:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20190327_1517'),
        ('movies', '0033_remove_groupusers_group_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='groupusers',
            unique_together=set([('user', 'group')]),
        ),
    ]
