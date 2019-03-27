#from django.views.generic import TemplateView
import csv, io
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Movie, TopMovies, UserDemographics, UserRatings,GroupInfo
from accounts.models import UserProfile
from tmdbv3api import TMDb
import pandas as pd
from tmdbv3api import Movie as tmdb_movie
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from scipy.spatial.distance import cosine
from django.http import HttpResponse
from .forms import *

def GroupView(request):
    template_name = 'movies/create_group.html'
    form = CreateGroup(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/account/profile')
    args = {'form':form}
    return render(request, template_name, args)

def JoinGroup(request):
    template_name = 'movies/join_group.html'
    groups = GroupInfo.objects.order_by('group_name')
    args = {'groups':groups}

    return render(request, template_name, args)

def JoinButton(request, pk):
    g = GroupUsers(group = GroupInfo.objects.get(group_id=pk), user = UserProfile.objects.get(user_id=request.user))
    g.save()
    return redirect ('/movies/join_group')

def ViewGroup(request, pk):
    template_name = 'movies/group_details.html'
    groups = GroupInfo.objects.filter(group_id=pk)
    '''
    form = JoinGroup(request.POST)
    if form.is_valid():
        form.user_id = UserProfile.objects.get(user_id=request.user)
        form.group_id = GroupInfo.objects.filter(group_id=pk)
        form.save()
    '''
    #args = {'form':form}
    return render(request, template_name)

def MovieView(request):
    template_name = 'movies/movies.html'
    movies = Movie.objects.order_by('name')
    ratings = UserRatings.objects.all()
    args = {'movies': movies, 'ratings':ratings}
    return render(request, template_name, args)


def Top10(request):
    template_name = 'movies/movie_list.html'
    top_movies = TopMovies.objects.all()
    args = {'top_movies': top_movies}
    return render(request, template_name, args)

def Recommendations(request):
    template_name ='movies/recommendations.html'
    top_movies = TopMovies.objects.all()
    current_user = request.user.id
    user_info = UserProfile.objects.filter(user_id=current_user)
    for user in user_info:
        user_age = user.Age
        user_occupation = user.Occupation
        user_gender = user.Gender
    rec_movies = age_occupation(user_age, user_occupation)
    movies = []
    for mov in rec_movies:
        movies.append(mov[5])

    rec_movies2 = gender_age(user_age,user_gender)
    movies2= []
    for mov in rec_movies2:
        movies2.append(mov[5])

    rec_movies3 = gender_occupation(user_gender, user_occupation)
    movies3= []
    for mov in rec_movies3:
        movies3.append(mov[5])

    args = {'top_movies': top_movies, 'user_info':user_info, 'movies':movies, 'movies2':movies2, 'movies3':movies3}
    return render(request, template_name, args)

def MovieDetails(request, pk):
    template_name = 'movies/movie_details.html'
    tmdb = TMDb()
    tmdb.api_key = '69c1026aa20e6449c7a0f74f69dffd7d'
    tmdb.language = 'en'
    movie = tmdb_movie()
    m = movie.details(pk)
    movie_id = 2
    my_movies = Movie.objects.filter(tmdbId=pk)
    for movie in my_movies:
        movie_id = movie.movie_id

    lists = SimilarMovies(movie_id)
    list_data = []
    list_id = []
    for list in lists:
        list_data.append(list[5])
        list_id.append(int(list[4]))
    image = "https://image.tmdb.org/t/p/w1280"+ m.poster_path
    form = RatingForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = UserProfile.objects.get(user_id=request.user)
        post.movie = Movie.objects.get(movie_id=movie_id)
        post.tmdbId = pk
        post.save()
        return redirect('/account/profile')

    args = {'m':m, 'image':image, "lists":lists, "list_data":list_data, "list_id":list_id, "movie_id":movie_id, "form":form}
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

def age_occupation(age,occupation):
    users = pd.read_csv("data/users.csv")
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings2 = pd.merge(movies, ratings, on = 'movieId')
    information = pd.merge(ratings, users, on='userId')
    user_demo = information.loc[(information.Occupation == occupation)&(information.rating >= 2.5)&(information.Age == age)]
    movie_data = pd.merge(ratings, movies, on='movieId')
    ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
    user_avg_rating = pd.DataFrame(user_demo.groupby('movieId')['rating'].mean())
    user_avg_rating['count_ratings'] = user_demo.groupby('movieId')['rating'].count()
    hundred_most_voted = user_avg_rating.sort_values('count_ratings', ascending=False).head(50)
    top_10 = hundred_most_voted.sort_values('rating', ascending=False).head(10)
    links = pd.read_csv("data/links.csv")
    sim = pd.merge(top_10, links, on='movieId')
    sim = pd.merge(sim, movies, on='movieId')
    sim = sim.values
    return sim

def gender_age(age,gender):
    users = pd.read_csv("data/users.csv")
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings2 = pd.merge(movies, ratings, on = 'movieId')
    information = pd.merge(ratings, users, on='userId')
    user_demo = information.loc[(information.Gender == gender)&(information.rating >= 2.5)&(information.Age == age)]
    movie_data = pd.merge(ratings, movies, on='movieId')
    ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
    user_avg_rating = pd.DataFrame(user_demo.groupby('movieId')['rating'].mean())
    user_avg_rating['count_ratings'] = user_demo.groupby('movieId')['rating'].count()
    hundred_most_voted = user_avg_rating.sort_values('count_ratings', ascending=False).head(50)
    top_10 = hundred_most_voted.sort_values('rating', ascending=False).head(10)
    links = pd.read_csv("data/links.csv")
    sim = pd.merge(top_10, links, on='movieId')
    sim = pd.merge(sim, movies, on='movieId')
    sim = sim.values
    return sim

def gender_occupation(gender,occupation):
    users = pd.read_csv("data/users.csv")
    ratings = pd.read_csv("data/ratings.csv")
    movies = pd.read_csv("data/movies.csv")
    ratings2 = pd.merge(movies, ratings, on = 'movieId')
    information = pd.merge(ratings, users, on='userId')
    user_demo = information.loc[(information.Occupation == occupation)&(information.rating >= 3)&(information.Gender == gender)]
    movie_data = pd.merge(ratings, movies, on='movieId')
    ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
    ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
    user_avg_rating = pd.DataFrame(user_demo.groupby('movieId')['rating'].mean())
    user_avg_rating['count_ratings'] = user_demo.groupby('movieId')['rating'].count()
    hundred_most_voted = user_avg_rating.sort_values('count_ratings', ascending=False).head(50)
    top_10 = hundred_most_voted.sort_values('rating', ascending=False).head(10)
    links = pd.read_csv("data/links.csv")
    sim = pd.merge(top_10, links, on='movieId')
    sim = pd.merge(sim, movies, on='movieId')
    sim = sim.values
    return sim
