from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=10, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
