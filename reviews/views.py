from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Review, Room
import json

# Create your views here.

def reviews(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            review = Review()
            review.room_id = request.POST.get()
            review.contents = request.POST.get("contents")
            review.user_id = request.user.id
            review.save()

            pass
        else:
            return redirect('accounts:signin')
    else:
        reviews = Review.objects.all().order_by("created_at").reverse()
        context = {
            'reviews' : reviews
        }
        return render(request, 'reviews.html', context)

def edit_review(request, article_id):
    article = Article.objects.get(id=article_id)
    if article.is_permitted(request.user.id):
        if request.method == "POST":
            article.contents = request.POST["contents"]
            article.save()
            return redirect('insta')
        else:
            context = {
                'article' : article
            }
            return render(request, 'article/edit.html', context)
    else:
        return redirect('insta')

def delete_review(request, article_id):
    article = Article.objects.get(id=article_id)
    if article.is_permitted(request.user.id):
        article.delete()
        return redirect('insta')
    else:
        return redirect('insta')


