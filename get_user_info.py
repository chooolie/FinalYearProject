import sys, os
import pandas as pd
import datetime
import django
django.setup()
# Inspiration from https://github.com/aakashsethi20/MovieScope
#Get user demographic information
#Not used in the end
from movies.models import UserDemographics
#in dbshell run delete from  movies_topmovies;
#exec(open('get_movies.py').read())

def save_movie_from_row(movie_row):
    movie = UserDemographics()
    movie.user_Id = movie_row[0]
    movie.Gender = movie_row[1]
    movie.Age = movie_row[2]
    movie.Occupation = movie_row[3]
    movie.save()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        #print "Reading from file " + str(sys.argv[1])
        movies_df = pd.read_csv('data/users.csv')

        movies_df.apply(
            save_movie_from_row,
            axis=1
        )

        print ("There are {} movies".format(UserDemographics.objects.count()))

    else:
        print ("Please, provide movie file path")
