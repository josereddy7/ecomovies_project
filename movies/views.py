from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Movie
from .tmdb import fetch_movie_details
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

watchlist = []

def recommend_movies(request):
    selected_genre = request.GET.get('genre', '')
    movies = Movie.objects.all()

    if selected_genre and selected_genre != "All":
        movies = movies.filter(genre__iexact=selected_genre)

    genres = Movie.objects.values_list('genre', flat=True).distinct()
    genres = sorted(set([g for g in genres if g]))  # filter empty/None

    if request.method == "POST":
        input_title = request.POST.get("movie_title")
        df = pd.DataFrame(list(movies.values('id', 'title', 'genre', 'description', 'poster_path', 'rating', 'year')))

        if df.empty or 'title' not in df.columns:
            return render(request, 'movies/recommend.html', {
                'recommended': [],
                'genres': genres,
                'selected_genre': selected_genre,
                'message': 'No movie data found.'
            })

        df = df[df['description'].str.strip().astype(bool)].drop_duplicates(subset='description')
        match = df.index[df['title'].str.lower() == input_title.lower()]

        if match.empty:
            movie_data = fetch_movie_details(input_title)
            if movie_data and movie_data['description'].strip():
                if not Movie.objects.filter(title__iexact=movie_data['title']).exists():
                    Movie.objects.create(**movie_data)
                movies = Movie.objects.all()
                if selected_genre and selected_genre != "All":
                    movies = movies.filter(genre__iexact=selected_genre)
                df = pd.DataFrame(list(movies.values('id', 'title', 'genre', 'description', 'poster_path', 'rating', 'year')))
                df = df[df['description'].str.strip().astype(bool)].drop_duplicates(subset='description')
                match = df.index[df['title'].str.lower() == movie_data['title'].lower()]
            else:
                return render(request, 'movies/recommend.html', {
                    'recommended': [],
                    'genres': genres,
                    'selected_genre': selected_genre,
                    'message': 'Movie not found in TMDB or missing data.'
                })

        if match.empty:
            return render(request, 'movies/recommend.html', {
                'recommended': [],
                'genres': genres,
                'selected_genre': selected_genre,
                'message': 'Movie still not found after fetching.'
            })

        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['description'])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        idx = match[0]
        sim_scores = sorted(list(enumerate(cosine_sim[idx])), key=lambda x: x[1], reverse=True)[1:6]
        recommended = [df.iloc[i[0]] for i in sim_scores]

        return render(request, 'movies/recommend.html', {
            'recommended': recommended,
            'selected': input_title,
            'genres': genres,
            'selected_genre': selected_genre
        })

    return render(request, 'movies/recommend.html', {
        'movies': movies,
        'genres': genres,
        'selected_genre': selected_genre
    })

from django.shortcuts import redirect
from django.urls import reverse

# Demo: in-memory list (replace with DB logic if needed)
watchlist = []

def add_to_watchlist(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
        if movie not in watchlist:
            watchlist.append(movie)
    except Movie.DoesNotExist:
        pass
    return redirect(reverse('recommend_movies'))
