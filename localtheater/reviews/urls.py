from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('reviews/', views.reviews, name="reviews"),
    path('reviews/submit/', views.submit_review, name="submit_review"),
    path('reviews/<int:review_id>/edit/', views.edit_review, name="edit_review"),
    path('reviews/<int:review_id>/delete/', views.delete_review, name="delete_review"),
]
