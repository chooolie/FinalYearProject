from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout, password_reset

urlpatterns = [
    url(r'^login/$', login, {'template_name':'accounts/login.html'}, name = 'login'),
    url(r'^logout/$', logout, {'template_name':'accounts/logout.html'}, name = 'logout'),
    url(r'^register/$',views.register, name='register'),
    url(r'^profile/$',views.view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$',views.view_profile, name='view_other_user'),
    url(r'^profile/edit/$',views.edit_profile, name='edit_profile'),
    url(r'^change-password/$',views.change_password, name='change_password')


]
