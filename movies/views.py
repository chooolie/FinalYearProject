#from django.views.generic import TemplateView
import csv, io
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Movie, TopMovies, UserDemographics, UserRatings,GroupInfo, GroupUsers, GroupMovieList
from .recommender import age_occupation, gender_age, gender_occupation, SimilarMovies
from .group_recommender import group_rec
from .collaborative import *
from accounts.models import UserProfile
from tmdbv3api import TMDb
import pandas as pd
from tmdbv3api import Movie as tmdb_movie
import pandas as pd
import numpy as np
import warnings
from django.contrib import messages
warnings.filterwarnings('ignore')
from scipy.spatial.distance import cosine
from django.http import HttpResponse
from .forms import *
from collections import Counter
from simple_search import search_filter
import operator
from django.db.models import Q
from django.db.models import F


def GroupVoteButton(request, pk, group):
    #This is used to give up votes to any movies added to the group movie list
    #Gets the group id and movie id which are unique together to increment the vote field
    mov = Movie.objects.get(tmdbId=pk)
    m_id = mov.movie_id
    m_details = GroupMovieList.objects.filter(group_id=group).filter(movie_id=m_id)
    m_details.update(vote= F('vote') +1)
    return redirect ('/movies/group_details/'+group)

def DeleteMovie(request,pk,group):
    #Allows users to delete movies in group watch list
    mov = Movie.objects.get(tmdbId=pk)
    m_id = mov.movie_id
    instance = GroupMovieList.objects.filter(group_id=group).filter(movie_id=m_id)
    instance.delete()
    return redirect ('/movies/group_details/'+group)

def LeaveGroup(request, group):
    #Allows users to leave groups
    user = UserProfile.objects.filter(user_id=request.user)
    instance = GroupUsers.objects.filter(group_id=group).filter(user_id=user)
    instance.delete()
    return redirect('/movies/join_group/')

def MyGroups(request):
    template_name = 'movies/my_groups.html'
    user = UserProfile.objects.filter(user_id=request.user)
    my_groups = GroupUsers.objects.filter(user_id=user)
    groupid=[]
    for group in my_groups:
        groupid = group.group_id

    name_groups = GroupInfo.objects.filter(group_id=groupid)

    name_groups = GroupInfo.objects.filter(group_id=groupid)
    args = {'my_groups':my_groups}
    return render(request, template_name, args)

def DownVoteButton(request, pk, group):
    #This is used to give down votes to any movies added to the group movie list
    #Gets the group id and movie id which are unique together to decrement vote field
    mov = Movie.objects.get(tmdbId=pk)
    m_id = mov.movie_id
    m_details = GroupMovieList.objects.filter(group_id=group).filter(movie_id=m_id)
    m_details.update(vote= F('vote') -1)
    return redirect ('/movies/group_details/'+group)

def GroupView(request):
    #Contains the form to create a group - takes a group name
    template_name = 'movies/create_group.html'
    form = CreateGroup(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/movies/join_group/')
    #users = User.objects.exclude(id=request.user.id)
    users = request.user
    args = {'form':form, 'users':users}
    return render(request, template_name, args)

def JoinGroup(request):
    #ALLOWS USER TO JOIN OR VIEW ANY CREATED GROUPS
    template_name = 'movies/join_group.html'
    groups = GroupInfo.objects.order_by('group_name')
    args = {'groups':groups}
    return render(request, template_name, args)


def JoinButton(request, pk):
    #WHEN SOMEONE CLICKS JOIN BUTTON FOR GROUPS
    try:
        g = GroupUsers(group = GroupInfo.objects.get(group_id=pk), user = UserProfile.objects.get(user_id=request.user), user_name = request.user.first_name)
        g.save()
        return redirect ('/movies/group_details/'+pk)
    except:
            messages.error(request, "You are already in this group!")
            return redirect ('/movies/join_group')

def ViewGroup(request, pk):
    #When a groups is clicked on - all the details
    #pk is group id
    #Recommender is in group_recommender.py
    template_name = 'movies/group_details.html'
    tmdb = TMDb()
    tmdb.api_key = '69c1026aa20e6449c7a0f74f69dffd7d'
    tmdb.language = 'en'
    people = GroupUsers.objects.filter(group_id=pk)
    group_name = GroupInfo.objects.filter(group_id=pk)
    group_movies = GroupMovieList.objects.filter(group_id=pk)
    m = []
    vote_score = []
    test = []
    #Getting movies for watch list
    for movie in group_movies:
        vote_score.append(movie.vote)
        my_movies = Movie.objects.filter(movie_id=movie.movie_id)
        for mov in my_movies:
            tmdbId = mov.tmdbId
        movs = tmdb_movie()
        m.append(movs.details(tmdbId))
        #Appending the vote count to the TMDB api link of top movies
    for index, i in enumerate(m):
        test.append((i,vote_score[index]))

    #Getting recommendations for group
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
    id = pk

    args = {'id':id, 'test':test, 'people':people, 'group_name':group_name, 'group_movies':group_movies, 'm':m, 'merging':merging,'all_mov':all_mov }
    return render(request, template_name,args)

def MovieView(request):
    #DISPLAY ALL MOVIES IN ALPHABETICAL ORDER
    template_name = 'movies/movies.html'
    movies = Movie.objects.all()
    ratings = UserRatings.objects.all()
    args = {'movies': movies, 'ratings':ratings}
    return render(request, template_name, args)

def SearchMovies(request):
    #ALLOW USER TO SEARCH MOVIES BY THE MOVIE NAME
    template_name = 'movies/search.html'
    query = request.GET['search_query']
    movies = Movie.objects.filter(name__contains=query)
    args = {'movies': movies}
    return render(request, template_name, args)

def Top10(request):
    #Display top 10 rated movies
    template_name = 'movies/movie_list.html'
    top_movies = TopMovies.objects.all()
    tmdb = TMDb()
    tmdb.api_key = '69c1026aa20e6449c7a0f74f69dffd7d'
    tmdb.language = 'en'
    movie = tmdb_movie()

    m = []
    for mov in top_movies:
        m.append(movie.details(mov.tmdbId))


    args = {'top_movies': top_movies, 'm':m}
    return render(request, template_name, args)

def Recommendations(request):
    #Get recommendations for the single user
    #All recommending functions are in recommender.py
    template_name ='movies/recommendations.html'
    current_user = request.user.id
    user_info = UserProfile.objects.filter(user_id=current_user)
    #get users demographics to pass to recommender
    for user in user_info:
        user_age = user.Age
        user_occupation = user.Occupation
        user_gender = user.Gender

    #Recommendations based on age and occupation
    rec_movies = age_occupation(user_age, user_occupation)
    movies = []
    for mov in rec_movies:
        movies.append(int(mov[4]))

    #Recommendations based on age and gender
    rec_movies2 = gender_age(user_age,user_gender)
    movies2= []
    for mov in rec_movies2:
        movies2.append(int(mov[4]))

    #Recommendations based on occupation and gender
    rec_movies3 = gender_occupation(user_gender, user_occupation)
    movies3= []
    for mov in rec_movies3:
        movies3.append(int(mov[4]))

    #Find most frequent movies that come up out of 3 above
    most_frequent = []
    most_frequent.extend(movies)
    most_frequent.extend(movies2)
    most_frequent.extend(movies3)
    recommendations = [word for word, word_count in Counter(most_frequent).most_common(10)]

    all_movies = []
    #Allow for the recommended movies to be clickable

    for mov in recommendations:
        my_movies = Movie.objects.filter(tmdbId=mov)
        for movie in my_movies:
            movie_id = movie.movie_id
            name = movie.name
            genre = movie.genre
            tmdb = movie.tmdbId
        all_movies.append([movie_id,name,genre,tmdb])

    try:
        args = { 'user_info':user_info, 'movies':movies, 'movies2':movies2, 'movies3':movies3, 'recommendations':recommendations, 'mov':mov, 'all_movies':all_movies}
        return render(request, template_name, args)
    except:
        messages.error(request, "You must enter your details first")
        return redirect('/account/adding_details/')

def MovieDetails(request, pk):
    #Accessing the TMDB API
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

    #Get the similar movies from recommender.py
    lists = SimilarMovies(movie_id)
    list_data = []
    list_id = []
    for list in lists:
        list_data.append(list[5])
        list_id.append(int(list[4]))

    try:
        image = "https://image.tmdb.org/t/p/w1280"+ m.poster_path
    except:
        image = "https://shenandoahcountyva.us/bos/wp-content/uploads/sites/4/2018/01/picture-not-available-clipart-12.jpg"
    #Get the rating from the user
    form = RatingForm(request.POST or None)
    try:
        if form.is_valid():
            post = form.save(commit=False)
            post.user = UserProfile.objects.get(user_id=request.user)
            post.movie = Movie.objects.get(movie_id=movie_id)
            post.tmdbId = pk
            post.save()
            return redirect('/account/profile')
    except:
        messages.error(request, "You have already rated this movie")
        return redirect('/movies/movie_details/' +pk)

    #Allow users to add current movie to any group
    movie_form = AddMovieToGroup(request.POST or None)
    try:
        if movie_form.is_valid():
            post2 = movie_form.save(commit=False)
            post2.user = UserProfile.objects.get(user_id=request.user)
            post2.movie = Movie.objects.get(movie_id=movie_id)
            post2.save()
            groupId = post2.group_id
            return redirect('/movies/join_group')
    except:
        messages.error(request, "This movie has already been added")
        return redirect('/movies/movie_details/' +pk)

    args = { 'm':m, 'image':image, "lists":lists, "list_data":list_data, "list_id":list_id, "movie_id":movie_id, "form":form, "movie_form":movie_form, "movie_id": movie_id}
    return render(request, template_name,args)

def CollabRecommendations(request):
    template_name ='movies/recommendations2.html'
    users_id = UserProfile.objects.filter(user_id=request.user)
    for u in users_id:
        id = u.id
    user1_rec = get_movies(id)
    df_rec = pd.DataFrame(data= { 'movieId':user1_rec})
    rec= [word for word, word_count in Counter(user1_rec).most_common(10)]

    all_movies = []
    #Allow for the recommended movies to be clickable
    for mov in rec:
        my_movies = Movie.objects.filter(movie_id=mov)
        for movie in my_movies:
            movie_id = movie.movie_id
            name = movie.name
            genre = movie.genre
            tmdb = movie.tmdbId
        all_movies.append([movie_id,name,genre,tmdb])

    voted = []
    ratings = UserRatings.objects.filter(user_id=id)
    for mov in ratings:
        my_movs = Movie.objects.filter(movie_id=mov.movie_id)
        for m in my_movs:
            v_movie_id = m.movie_id
            v_name = m.name
            v_genre = m.genre
            v_tmdb = m.tmdbId
        v_rating = mov.rating
        voted.append([v_movie_id,v_name,v_genre,v_tmdb,v_rating])
    args = { 'voted':voted,'all_movies':all_movies, 'ratings':ratings}

    return render(request, template_name, args)
