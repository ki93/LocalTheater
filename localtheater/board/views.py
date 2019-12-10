from django.shortcuts import render,redirect
from django.core import serializers
# .models 현재 폴더 모델의 Article
from django.http.response import HttpResponse
from .models import Movie, Theater, Room, TheaterMovie, Timetable
import json
# DRF
# Create your views here.

def index(request):
    return render(request, 'index.html')

def findmovie(request):
    return render(request, 'index.html')

def findbyname(request):
    if request.GET.get("type") == "title":
        title = request.GET.get("title")
        theaters = Movie.objects.get(title=title).theaters.all()
        remain_count = 5-theaters.count()%5
        context = {
            'theaters' : theaters,
            'remain_count' : range(remain_count),
        }
        return render(request, 'categorypage.html', context)
    else:
        id_string = request.GET.get('selected')
        movie_id = id_string.split('-')[0]
        theater_id = list(map(int,id_string.split('-')[1:-1]))
        movie_title = Movie.objects.get(id=movie_id).title
        theaters = Theater.objects.filter(id__in=theater_id)
        theatermovies = TheaterMovie.objects.filter(movie_id__in=movie_id, theater_id__in=theater_id)
        print(movie_id)
        print(theaters)
        print(movie_title) 
        print(theatermovies)
        context = {
            'theatermovies' : theatermovies,
        }
        return render(request,'result.html', context)

def findmoviename(request):
    movies = Movie.objects.all().values('title', 'id')
    remain_count = 5-movies.count()%5
    context = {
        'remain_count' : range(remain_count),
        'movies' : movies,
    }
    return render(request, 'findnamepage.html', context)

def adminpage(request):
    if request.user.is_staff:
        if request.method == "POST":
                theater, created = Theater.objects.update_or_create(
                    company = request.POST.get("company"),
                    branch = request.POST.get("branch"),
                    lat = request.POST.get("lat"),
                    lon = request.POST.get("lon"),
                )
                
                movie, created = Movie.objects.update_or_create(
                    title = request.POST.get("title"),
                )
                room, created = Room.objects.update_or_create(
                    theater_id = theater.id,
                    name = request.POST.get("name"),
                    category = request.POST.get("category"),
                )
                theatermovie, created = TheaterMovie.objects.update_or_create(
                    theater_id = theater.id,
                    movie_id = movie.id,
                )
                start_time_date = request.POST.get("start_time_date")
                start_time_time = request.POST.get("start_time_time")
                timetable, created = Timetable.objects.update_or_create(
                    start_time = " ".join([start_time_date,start_time_time]),
                    room_id = room.id,
                    playinfo_id = theatermovie.id,
                )
                return redirect('board:adminpage')
        else:
            theaters = Theater.objects.all().order_by("-created_at")
            for theater in theaters:
                print(theater.get_all_movies)
                print(theater.movies.all())
                for movie in theater.movies.all():
                    print(theater.movies.all())
                    print(movie.title)
            context = {
                'theaters' : theaters,
            }
            return render(request, 'adminpage.html', context)
    else:
        return redirect('accounts:signin')    

def theater_delete(request):
    theater_id = request.POST["theater_id"]
    theater = Theater.objects.get(id=theater_id)
    if request.user.is_staff:
        theater.delete()
        context = {
                'theater_id' : theater_id,
            }
        return HttpResponse(json.dumps(context), status=200, content_type="application/json")
    else:
        return HttpResponse(status=401)
