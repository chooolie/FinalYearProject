#from django.views.generic import TemplateView
import csv, io
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Movie, TopMovies
from tmdbv3api import TMDb
import pandas as pd
from tmdbv3api import Movie as tmdb_movie
import pandas as pd
import numpy as np
import warnings
from scipy.spatial.distance import cosine
from django.http import HttpResponse
warnings.filterwarnings('ignore')


def MovieView(request):
    template_name = 'movies/movies.html'
    movies = Movie.objects.order_by('name')
    args = {'movies': movies}
    return render(request, template_name, args)

def Top10(request):
    template_name = 'movies/movie_list.html'
    top_movies = TopMovies.objects.all()
    args = {'top_movies': top_movies}
    return render(request, template_name, args)

def Recommendations(request):
    template_name ='movies/recommendations.html'
    top_movies = TopMovies.objects.all()
    args = {'top_movies': top_movies}
    return render(request, template_name, args)

def MovieDetails(request, pk):
    template_name = 'movies/movie_details.html'
    tmdb = TMDb()
    tmdb.api_key = '69c1026aa20e6449c7a0f74f69dffd7d'
    tmdb.language = 'en'
    movie = tmdb_movie()
    m = movie.details(pk)
    movie_id = 2
    my_movies = Movie.objects.filter(movie_id=pk)
    for movie in my_movies:
        movie_id = movie.movie_id

    lists = SimilarMovies(movie_id)
    #lists = lists[0]
    list_data = []
    list_id = []
    for list in lists:
        list_data.append(list[5])
        list_id.append(int(list[4]))
    image = "https://image.tmdb.org/t/p/w1280"+ m.poster_path
    args = {'m':m, 'image':image, "lists":lists, "list_data":list_data, "list_id":list_id}
    return render(request, template_name,args)

def SimilarMovies(Movie_Id):
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.merge(ratings, movies, on='movieId')
    avg_rating = pd.DataFrame(ratings.groupby('movieId')['rating'].mean())
    avg_rating['count_ratings'] = ratings.groupby('movieId')['rating'].count()
    ratings_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')
    user_rating = ratings_matrix[Movie_Id]
    similar_to = ratings_matrix.corrwith(user_rating)
    corr = pd.DataFrame(similar_to, columns=['Correlation'])
    corr.dropna(inplace=True)
    corr = corr.join(avg_rating['count_ratings'])
    similar = corr[corr['count_ratings'] > 50].sort_values(by='Correlation', ascending=False).head(10)
    links = pd.read_csv("data/links.csv")
    sim = pd.merge(similar, links, on='movieId')
    sim = pd.merge(sim, movies, on='movieId')
    lists = sim['title'].values
    sim = sim.values
    return sim
