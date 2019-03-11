#from django.views.generic import TemplateView
import csv, io
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Movie, TopMovies


def MovieView(request):
    template_name = 'movies/movies.html'
    movies = Movie.objects.all()
    args = {'movies': movies}
    #context = {'MovieView': MovieView}
    return render(request, template_name, args)

def Top10(request):
    template_name = 'movies/movie_list.html'
    top_movies = TopMovies.objects.all()
    counter = 1
    args = {'top_movies': top_movies, 'counter':counter}
    return render(request, template_name, args)
