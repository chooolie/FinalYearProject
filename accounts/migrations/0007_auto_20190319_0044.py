# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-19 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20190319_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='Age',
            field=models.CharField(choices=[('Under18', 'Under18'), ('18-24', '18-24'), ('25-34', '25-34'), ('35-44', '35-44'), ('45-49', '45-49'), ('50-55', '50-55'), ('56+', '56+')], max_length=2),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='Occupation',
            field=models.CharField(choices=[('K-12student', 'K-12student'), ('self-employed', 'Self Employed'), ('scientist', 'scientist'), ('executive/managerial', 'executive/managerial'), ('writer', 'writer'), ('homemaker', 'homemaker'), ('academic/educator', 'academic/educator'), ('scientist', 'scientist'), ('doctor/health care', 'doctor/health care'), ('sales/marketing', 'sales/marketing'), ('clerical/admin', 'clerical/admin'), ('programmer', 'programmer'), ('technician/engineer', 'technician/engineer'), ('college/grad student', 'college/grad student'), ('artist', 'artist'), ('tradesman/craftsman', 'tradesman/craftsman'), ('retired', 'retired'), ('unemployed', 'unemployed'), ('other', 'other')], max_length=20),
        ),
    ]
