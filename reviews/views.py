from django.shortcuts import render, redirect

# Create your views here.

def reviews(request):
    return render(request, 'index.html')

def submit_review(request):
    return render(request, 'index.html')

def edit_review(request):
    return render(request, 'index.html')

def delete_review(request):
    return render(request, 'index.html')
