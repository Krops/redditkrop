from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# Create your views here.
@login_required
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['url']:
            post = Post()
            post.title = request.POST['title']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                post.url = request.POST['url']
            else:
                post.url = 'http://' + request.POST['url']
            post.pub_date = timezone.now()
            post.author = request.user
            post.save()
            return redirect('home')
        else:
            return render(request, 'posts/create.html', {'error': 'ERROR: You must include title and url'})
    else:
        return render(request, 'posts/create.html')

def home(request):
    posts = Post.objects.order_by('-pub_date')
    return render(request, 'posts/home.html', {'posts':posts})

def user_posts(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user.id)
    return render(request, 'posts/user_posts.html', {'posts':posts, 'user':user})

def upvote(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.votes_total +=1
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def downvote(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.votes_total -=1
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))