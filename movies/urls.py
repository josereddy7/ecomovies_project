from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_movies, name='recommend_movies'),
    path('watchlist/add/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
]
