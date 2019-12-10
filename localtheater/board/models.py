from django.db import models
from django.conf import settings

# Create your models here.

class Theater(models.Model):
    company = models.CharField(max_length=30)
    branch = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # DecimalField 9글자 십진수 소수자리 6개까지
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    def get_all_movies(self):
        return self.movies.title
class Movie(models.Model):
    theaters = models.ManyToManyField(Theater, through='TheaterMovie', related_name='movies')
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Room(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20)

class TheaterMovie(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class Timetable(models.Model):
    start_time = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    playinfo = models.ForeignKey(TheaterMovie, on_delete=models.CASCADE)


