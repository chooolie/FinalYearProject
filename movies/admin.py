from django.contrib import admin
from movies.models import  *

# Register your models here.
admin.site.register(Movie)
admin.site.register(TopMovies)
admin.site.register(UserRatings)
admin.site.register(GroupInfo)
admin.site.register(GroupUsers)
