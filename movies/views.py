from django.views.generic import TemplateView
import csv, io
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .models import Movie

class MovieView(TemplateView):
    template_name = 'movies/movies.html'

def movie_list(request):
	movie_list = Movie.objects.order_by('-movie_id')
	context = {'movie_list': movie_list}
	return render(request, 'reviews/movie_list.html', context)
