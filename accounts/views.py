from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                login(request, user)
                return render(request, 'accounts/signup.html')
            except IntegrityError:
                return render(request, 'accounts/signup.html', {'error': 'Username is exist'})
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords didn\'t match'})
    else:
        return render(request, 'accounts/signup.html')


def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                if request.POST['next'] is not None:
                    return redirect(request.POST['next'])
            return render(request, 'accounts/login.html')
        else:
            return render(request, 'accounts/login.html', {'error': 'Passwords or user didn\'t match'})
    else:
        return render(request, 'accounts/login.html')
