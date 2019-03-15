import sys, os
import pandas as pd
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moviescope.settings")

import django
django.setup()
# Inspiration from https://github.com/aakashsethi20/MovieScope

from movies.models import Movie
#in dbshell run delete from  movies_topmovies;
#exec(open('get_movies.py').read())

def save_movie_from_row(movie_row):
    movie = Movie()
    movie.movie_id = movie_row[0]
    movie.tmdbId = movie_row[1]    
    movie.name = movie_row[2]
    movie.genre = movie_row[3]
    movie.save()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        #print "Reading from file " + str(sys.argv[1])
        movies_df = pd.read_csv('data/movies_links.csv')

        movies_df.apply(
            save_movie_from_row,
            axis=1
        )

        print ("There are {} movies".format(Movie.objects.count()))

    else:
        print ("Please, provide movie file path")
