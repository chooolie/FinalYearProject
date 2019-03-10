from django.db import models

# Create your models here.
class Movie(models.Model):
	movie_id = models.IntegerField(primary_key=True)
	name = models.CharField("Movie name", max_length=300)
	genre = models.CharField("Movie genre", default="", max_length=300)
