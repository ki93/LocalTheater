from django.shortcuts import render,redirect
# .models 현재 폴더 모델의 Article
from django.http.response import HttpResponse
from .models import Movie, Theater
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')

def findmovie(request):
    return render(request, 'index.html')

def adminpage(request):
    if request.method == "POST":
        if request.user.is_staff:
            if request.POST["formname"] == "theater":
                theater = Theater()
                theater.company = request.POST["company"]
                theater.branch = request.POST["branch"]
                theater.num = request.POST["num"]
                theater.category = request.POST["category"]
                theater.lat = request.POST["lat"]
                theater.lon = request.POST["lon"]
                theater.save()
                context = {
                'id' : theater.id,
                'company' : theater.company,
                'branch' : theater.branch,
                'num' : theater.num,
                'category' : theater.category,
                'lat' : theater.lat,
                'lon' : theater.lon,
                }
                return HttpResponse(json.dumps(context), content_type="application/json")
            elif request.POST["formname"] == "movie":
                movie = Movie()
                movie.theater_id_id = request.POST["theater_id"]
                movie.movie_name = request.POST["movie_name"]
                movie.show_time = " ".join([request.POST["show_time_date"],request.POST["show_time_time"]])
                movie.save()
                context = {
                    'theater_id' : movie.theater_id_id,
                    'movie_name' : movie.movie_name,
                    'show_time' : movie.show_time,
                }
                return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            context = {
                'status' : 401,
                'message' : "Need to Sign in"
            }
            return HttpResponse(json.dumps(context), status=401, content_type="application/json")
    else:
        theater = Theater.objects.all().order_by("created_at").reverse()
        context = {
            'theaters' : theater
        }
        return render(request, 'adminpage.html', context)

    