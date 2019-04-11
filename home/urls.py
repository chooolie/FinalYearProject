from django.conf.urls import url
from home.views import HomeView
from . import views

urlpatterns = [
    url(r'^$', HomeView.as_view(), name = 'review'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.add_del_friends, name='add_del_friends')
]
