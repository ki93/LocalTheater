from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_signin
from django.contrib.auth import logout as auth_signout
# 상속 받아 만든 CreateUserForm import
from .models import CreateUserForm
# Create your views here.

def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_signin(request, form.get_user())
            return redirect('board:index')
        else:
            return render(request, 'signin.html')
    else:
        if request.user.is_authenticated:
            return redirect('board:index')
        else:
            return render(request, 'signin.html')

def signout(request):
    auth_signout(request)
    return redirect('board:index')

def signup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            auth_signin(request, user)
            return redirect('board:index')
        else:
            return render(request, 'signup.html')
    else:
        if request.user.is_authenticated:
            return redirect('board:index')
        else:
            return render(request, 'signup.html')