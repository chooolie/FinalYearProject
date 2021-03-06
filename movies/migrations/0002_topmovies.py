# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-11 16:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopMovies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=3, verbose_name='rating')),
                ('count_ratings', models.IntegerField(default=0, verbose_name='count_ratings')),
                ('movie_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
    ]
