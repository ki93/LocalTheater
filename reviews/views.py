from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .models import Review, Room
from board.models import Theater
import json

# Create your views here.

def reviews(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            review = Review()
            review.room_id = request.POST.get("room_id")
            review.contents = request.POST.get("contents")
            review.user_id = request.user.id
            review.save()
            context = {
                'review' : review,
            }
            return render(request, 'reviewprepend.html', context)
        else:
            return redirect('accounts:signin')
    else:
        reviews = Review.objects.all().order_by("-created_at")
        context = {
            'reviews' : reviews,
        }
        return render(request, 'reviews.html', context)

def delete_review(request):
    review_id = request.POST.get("review_id")
    review = Review.objects.get(id=review_id)
    print(review_id)
    if review.user_id == request.user.id:
        review.delete()
        return HttpResponse(review_id)
    else:
        return redirect('reviews:reviews')

def review_company(request):
    return render(request, 'reviewcompany.html')

def review_branch(request):
    company_name = request.GET.get("company_name")
    theaters = Theater.objects.filter(company=company_name)
    context = {
        'theaters' : theaters,
    }
    return render(request, 'reviewbranch.html', context)

def review_room(request):
    company_name = request.GET.get("company_name")
    branch_name = request.GET.get("branch_name")
    theater = Theater.objects.filter(company=company_name,branch=branch_name).first()
    rooms = theater.room_set.all()
    context = {
        'rooms' : rooms,
    }
    return render(request, 'reviewroom.html', context)

