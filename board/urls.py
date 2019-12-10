from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path('', views.index, name="index"),
    path('findmovie/location/select', views.selectBranch, name="searchMovieByThreaterLocation"),
    path('findmovie/location/result', views.viewMovieInfoByBranch, name="resultMovieInfoByLocation"),
    path('findmovie/', views.findmovie, name="findmovie"),
    path('findmoviename/', views.findmoviename, name="findmoviename"),
    path('findbyname/', views.findbyname, name="findbyname"),
    path('adminpage/', views.adminpage, name="adminpage"),
    path('adminpage/theater_delete/', views.theater_delete, name="theater_delete"),
]

