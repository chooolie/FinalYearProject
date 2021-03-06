from django.db import models
from .choices import *
from accounts.models import UserProfile
from django.contrib.auth.models import User
from updown.fields import RatingField


# All models for movie related information
#Updates database and must run migrations to get to work

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

class UserDemographics(models.Model):
	userdemo_id = models.IntegerField("id", primary_key=True)
	Gender = models.CharField("gender", max_length=2, default="M")
	Age = models.CharField("age", max_length=50, default="18-24")
	Occupation = models.CharField("job", max_length= 100, default="other")

class UserRatings(models.Model):
	user = models.ForeignKey(UserProfile, default = 1, on_delete=models.CASCADE )
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	rating =  models.FloatField(choices=RATING_CHOICE,default = 2.5)
	tmdbId =  models.IntegerField("TmdbId",default = 1)

	class Meta:
		unique_together = ("user", "movie")

class GroupInfo(models.Model):
	group_id = models.IntegerField("id", primary_key=True)
	group_name = models.CharField("name", max_length=50, unique=True )
	def __str__(self):
	   return self.group_name

class GroupUsers(models.Model):
	group =  models.ForeignKey(GroupInfo, on_delete=models.CASCADE )
	user =   models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	user_name = models.CharField("name", max_length=100, default="jane doe")
	class Meta:
		unique_together = ("user", "group")

class GroupMovieList(models.Model):
	group =  models.ForeignKey(GroupInfo,choices = GroupInfo._meta.get_field('group_name').choices, on_delete=models.CASCADE )
	user =   models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	vote = models.IntegerField("vote", default=0)
	class Meta:
		unique_together = ("movie", "group")
