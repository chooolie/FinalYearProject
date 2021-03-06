# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-18 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190318_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='Age',
            field=models.CharField(choices=[(1, 'Under18'), (2, '18-24'), (3, '25-34'), (4, '35-44'), (5, '45-49'), (6, '50-55'), (7, '56+')], default='18-24', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Gender',
            field=models.CharField(choices=[(1, 'F'), (2, 'M'), (3, 'Other')], default='M', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Occupation',
            field=models.CharField(choices=[(1, 'K-12student'), (2, 'self-employed'), (3, 'scientist'), (4, 'executive/managerial'), (5, 'writer'), (6, 'homemaker'), (7, 'academic/educator'), (8, 'scientist'), (9, 'doctor/health care'), (10, 'sales/marketing'), (11, 'clerical/admin'), (12, 'programmer'), (13, 'technician/engineer'), (14, 'college/grad student'), (15, 'artist'), (16, 'tradesman/craftsman'), (17, 'retired'), (18, 'unemployed'), (19, 'other')], default='other', max_length=20),
        ),
    ]
