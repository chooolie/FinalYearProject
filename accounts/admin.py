from django.contrib import admin
from accounts.models import UserProfile
# Register your models here.
#admin.site.register(UserProfile)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'phone', 'user_info')
    #add the information about the users to the main page about users
    def user_info(self, obj):
        return obj.description

    def get_queryset(self, request):
        #changing order of users in the admin
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-city')
        return queryset

    user_info.short_description = 'Info'

admin.site.register(UserProfile,UserProfileAdmin)
