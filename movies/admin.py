from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from movies.models import  *

# Register your models here.
admin.site.register(Movie)
admin.site.register(TopMovies)
#admin.site.register(UserRatings)
admin.site.register(GroupInfo)
admin.site.register(GroupUsers)

@admin.register(UserRatings)
class ViewAdmin(ImportExportModelAdmin):
    pass
