from django.conf.urls import url
#from movies.views import MovieView

from . import views

urlpatterns = [
    url(r'^view_movies/$',views.MovieView, name='movies'),
    url(r'^top10/$',views.Top10, name='top_movies'),
    url(r'^movie_details/(?P<pk>\d+)/$',views.MovieDetails, name='view'),
    url(r'^recommendations/$',views.Recommendations, name='recommendations'),

]
