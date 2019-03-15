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

#Will eventually be linked to users on the web app
#However dont have these users signed up yet
#Made it into its own ID for the training data

class UserDemographics(models.Model):
	userId = models.IntegerField("id", primary_key=True)
	Gender = models.CharField("gender", max_length=2, default="M")
	Age = models.CharField("age", max_length=50, default="18-24")
	Occupation = models.CharField("job", max_length= 100, default="other")

class UserRatings(models.Model):
	userId = models.ForeignKey(UserDemographics, on_delete=models.CASCADE )
	movieId = models.ForeignKey(Movie, on_delete=models.CASCADE)
	rating =  models.IntegerField("id",default = 2)
	tmdbId =  models.IntegerField("id",default = 1)

#exec(open('get_movies.py').read())
