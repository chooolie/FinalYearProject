from django.conf.urls import url
from movies.views import MovieView
from . import views

urlpatterns = [
    url(r'^view_movies/$', MovieView.as_view(), name = 'movies')

]
