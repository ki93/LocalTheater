

from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('reviews/show/', views.reviews, name="reviews"),
    path('reviews/delete/', views.delete_review, name="delete_review"),
    path('reviews/review_company/', views.review_company, name="review_company"),
    path('reviews/review_branch/', views.review_branch, name="review_branch"),
    path('reviews/review_room/', views.review_room, name="review_room"),
]
