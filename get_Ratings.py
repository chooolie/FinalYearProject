import sys, os
import pandas as pd
import datetime
import django
django.setup()
# Inspiration from https://github.com/aakashsethi20/MovieScope
#Python file to read in ratings from CSV file into the model

from movies.models import UserRatings, UserDemographics, Movie
#in dbshell run delete from  movies_topmovies;
#exec(open('get_movies.py').read())

def save_movie_from_row(movie_row):
    movie = UserRatings()
    movie.userdemo_id_id = int(movie_row[0])
    movie.movie_id_id = int(movie_row[1])
    movie.rating = int(movie_row[2])
    movie.tmdbId = int(movie_row[3])
    movie.save()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        #print "Reading from file " + str(sys.argv[1])
        movies_df = pd.read_csv('data/ratings.csv')

        movies_df.apply(
            save_movie_from_row,
            axis=1
        )

        print ("{} Movies added".format(UserRatings.objects.count()))

    else:
        print ("nvalid path")
