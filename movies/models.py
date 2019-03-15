from django.db import models

# Create your models here.
class Movie(models.Model):
	movie_id = models.IntegerField("id",primary_key=True)
	tmdbId = models.IntegerField("id",default = 1)
	name = models.CharField("name", max_length=300)
	genre = models.CharField("genre", default="", max_length=300)

'''
CASCADE: When the referenced object is deleted,
also delete the objects that have references to it
'''

class TopMovies(models.Model):
	movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
	tmdbId = models.IntegerField("id",default = 1)
	rating = models.FloatField("rating", default = 3)
	count_ratings = models.IntegerField("count_ratings", default = 0)
	title = models.CharField("title", max_length=300, default= 'N/A')
	genre = models.CharField("genres", default="", max_length=300)

#exec(open('get_movies.py').read())
