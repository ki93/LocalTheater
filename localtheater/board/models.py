from django.db import models
from django.conf import settings

# Create your models here.

class Theater(models.Model):
    company = models.CharField(max_length=30)
    branch = models.CharField(max_length=50)
    num = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # DecimalField 9글자 십진수 소수자리 6개까지
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

class Movie(models.Model):
    theater_id = models.ForeignKey(Theater, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=100)
    show_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)