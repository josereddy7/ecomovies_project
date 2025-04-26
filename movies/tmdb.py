import requests

API_KEY = '9874a1b0c5dea93797b63e58f2d23703'  # your actual TMDB API key

def fetch_movie_details(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(url)
    data = response.json()

    if data.get('results'):
        movie = data['results'][0]
        return {
            'title': movie.get('title', 'Unknown'),
            'genre': 'Unknown',  # Simplified; can expand later with genre API
            'description': movie.get('overview', 'No description'),
            'poster_path': movie.get('poster_path', ''),
            'rating': movie.get('vote_average', 'N/A'),
            'year': movie.get('release_date', '')[:4] if movie.get('release_date') else ''
        }
    return None
