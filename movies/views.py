#from django.views.generic import TemplateView
import csv, io
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Movie, TopMovies, UserDemographics, UserRatings,GroupInfo, GroupUsers, GroupMovieList
from .recommender import age_occupation, gender_age, gender_occupation, SimilarMovies
from .group_recommender import group_rec
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
from collections import Counter
from simple_search import search_filter
import operator
from django.db.models import Q


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
    g = GroupUsers(group = GroupInfo.objects.get(group_id=pk), user = UserProfile.objects.get(user_id=request.user), user_name = request.user.first_name)
    g.save()
    return redirect ('/movies/join_group')

def ViewGroup(request, pk):
    #pk is group id
    template_name = 'movies/group_details.html'
    tmdb = TMDb()
    tmdb.api_key = '69c1026aa20e6449c7a0f74f69dffd7d'
    tmdb.language = 'en'
    people = GroupUsers.objects.filter(group_id=pk)
    group_name = GroupInfo.objects.filter(group_id=pk)
    group_movies = GroupMovieList.objects.filter(group_id=pk)
    m = []
    for movie in group_movies:
        my_movies = Movie.objects.filter(movie_id=movie.movie_id)
        for mov in my_movies:
            tmdbId = mov.tmdbId
        movs = tmdb_movie()
        m.append(movs.details(tmdbId))


    merging = []
    for user in people:
        u_id = user.user_id
        user_info = UserProfile.objects.filter(id=u_id)
        for users in user_info:
            user_age = users.Age
            user_occupation = users.Occupation
        rec_movs = group_rec(user_age, user_occupation)
        rec_movs = rec_movs.index.values.tolist()
        merging.extend(rec_movs)
    all_mov= [word for word, word_count in Counter(merging).most_common(10)]

    args = {'people':people, 'group_name':group_name, 'group_movies':group_movies, 'm':m, 'merging':merging,'all_mov':all_mov}
    return render(request, template_name,args)

def MovieView(request):
    #DISPLAY ALL MOVIES IN ALPHABETICAL ORDER
    template_name = 'movies/movies.html'
    #movies = Movie.objects.order_by('name')
    #movies = Movie.objects.filter(name__contains='avengers')
    movies = Movie.objects.all()
    ratings = UserRatings.objects.all()
    args = {'movies': movies, 'ratings':ratings}
    return render(request, template_name, args)

def SearchMovies(request):
    template_name = 'movies/search.html'
    query = request.GET['search_query']
    movies = Movie.objects.filter(name__contains=query)
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
    form = RatingForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = UserProfile.objects.get(user_id=request.user)
        post.movie = Movie.objects.get(movie_id=movie_id)
        post.tmdbId = pk
        post.save()
        return redirect('/account/profile')

    movie_form = AddMovieToGroup(request.POST or None)
    if movie_form.is_valid():
        post2 = movie_form.save(commit=False)
        post2.user = UserProfile.objects.get(user_id=request.user)
        post2.movie = Movie.objects.get(movie_id=movie_id)
        post2.save()
        return redirect('/account/profile')

    args = {'m':m, 'image':image, "lists":lists, "list_data":list_data, "list_id":list_id, "movie_id":movie_id, "form":form, "movie_form":movie_form}
    return render(request, template_name,args)
