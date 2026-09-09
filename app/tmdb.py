import os, requests

from dotenv import load_dotenv

load_dotenv()

tmdb_api_token = os.getenv("TMDB_API_TOKEN")

def search_movie(title):
    url = "https://api.themoviedb.org/3/search/movie"
    headers = {
        "Authorization": f"Bearer {tmdb_api_token}"
    }
    parameters = {
        "query": title
    }
    response = requests.get(url, headers=headers, params=parameters)

    response.raise_for_status()
    results =  response.json()["results"]

    if not results:
        return None
    
    return results[0]

def get_poster_url(poster_path):
    if poster_path is None:
        return None

    return f"https://image.tmdb.org/t/p/w500{poster_path}"

def get_movie_poster(title):
    movie = search_movie(title)

    if movie is None:
        return None
    
    return get_poster_url(movie["poster_path"])

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {tmdb_api_token}"
    }

    parameters = {
        "append_to_response": "credits"
    }

    response = requests.get(url, headers=headers, params=parameters)
    response.raise_for_status()

    return response.json()

def get_movie_director(details):
    for person in details["credits"]["crew"]:
        if person["job"] == "Director":
            return person["name"]

    return None