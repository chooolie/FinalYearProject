# Create your views here.
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from home.forms import HomeForm
from home.models import Post, AddFriend
from django.contrib.auth.models import User

class HomeView(TemplateView):
    template_name = 'home/review.html'

    def get(self, request):
        form = HomeForm()
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        friend, created = AddFriend.objects.get_or_create(current_user=request.user)
        friends = friend.users.all()
        args =  {'form': form, 'posts': posts, 'users':users, 'friends':friends}
        return render(request, self.template_name, args)

    def post(self, request):
        form = HomeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            text = form.cleaned_data['post']
            form = HomeForm()
            return redirect ('review')

        args = {'form':form, 'text': text}
        return render(request, self.template_name, args)

def add_del_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        AddFriend.adding(request.user,new_friend)
    elif operation == 'remove':
        AddFriend.deleting(request.user,new_friend)
    return redirect ('review')
