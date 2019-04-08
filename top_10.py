import sys, os
import pandas as pd
import numpy as np
import django
django.setup()
from movies.models import TopMovies
#Function used to get the top 10 Movies based on the ratings
#- to update top 10 csv list
#exec(open('get_top_10.py').read())
#in dbshell run delete from  movies_topmovies;
#in django shell run exec(open('top_10_to_csv.py').read())

def get_top_10():
    #read in ratings csv file
    ratings = pd.read_csv("data/ratings.csv")
    #read in movie csv file
    movies = pd.read_csv("data/movies.csv")
    #read in links links
    links = pd.read_csv("data/links.csv")
    #ratings = pd.merge(ratings, movies, on='movieId')
    average_mean = ratings.rating.describe().iloc[[1]] #avg overall rating
    avg_rating = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())#avg rating of each movie
    #Get count of ammount of votes per movie and add to DF
    avg_rating['count_ratings'] = ratings.groupby('movieId')['rating'].count()
    top_ten_rated = avg_rating.sort_values('rating', ascending=False).head(10) # top ten rated movies
    ten_most_voted = avg_rating.sort_values('count_ratings', ascending=False).head(10) # top ten most voted
    hundred_most_voted = avg_rating.sort_values('count_ratings', ascending=False).head(100)
    top_10 = hundred_most_voted.sort_values('rating', ascending=False).head(10)
    top_10 = pd.merge(top_10, movies, on='movieId')
    top_10 = pd.merge(top_10, links, on='movieId')
    top_10= top_10.drop(columns='imdbId')
    return top_10

top10 = get_top_10()
top10.to_csv("data/top_10.csv", sep=',', index = False)
