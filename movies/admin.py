from django.contrib import admin
from movies.models import  Movie, TopMovies

# Register your models here.
admin.site.register(Movie)
admin.site.register(TopMovies)
