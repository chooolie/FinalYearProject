import sys, os
import pandas as pd
import django
django.setup()
# Inspiration from https://github.com/aakashsethi20/MovieScope
from movies.models import TopMovies

#To add new list
#in dbshell run delete from  movies_topmovies;
#in django shell run exec(open('top_10_to_csv.py').read())

def save_movie_from_row(movie_row):
    movie = TopMovies()
    movie.movie_id_id = movie_row[0]
    movie.rating = movie_row[1]
    movie.count_ratings = movie_row[2]
    movie.save()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        movies_df = pd.read_csv('data/top_10.csv')

        movies_df.apply(
            save_movie_from_row,
            axis=1
        )

        print ("There are {} movies".format(TopMovies.objects.count()))

    else:
        print ("Please, provide movie file path")
