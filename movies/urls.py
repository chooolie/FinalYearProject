from django.conf.urls import url
#from movies.views import MovieView

from . import views
#All the URLS for each view
urlpatterns = [
    url(r'^view_movies/$',views.MovieView, name='movies'),
    url(r'^top10/$',views.Top10, name='top_movies'),
    url(r'^movie_details/(?P<pk>\d+)/$',views.MovieDetails, name='view'),
    url(r'^recommendations/$',views.Recommendations, name='recommendations'),
    url(r'^create_group/$',views.GroupView, name='group'),
    url(r'^join_group/$',views.JoinGroup, name='join_group'),
    url(r'^group_details/(?P<pk>\d+)/$',views.ViewGroup, name='view_group'),
    url(r'^connect/(?P<pk>\d+)/$',views.JoinButton, name='join_button'),
    url(r'^searching/$',views.SearchMovies, name='searching'),
    url(r'^groupvote/(?P<pk>\d+)/(?P<group>\d+)/$',views.GroupVoteButton, name='groupvote'),
    url(r'^downvote/(?P<pk>\d+)/(?P<group>\d+)/$',views.DownVoteButton, name='downvote'),

]
