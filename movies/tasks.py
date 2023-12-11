# tasks.py
import requests
from imdb import Cinemagoer
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from movies.models import Movie, MovieView

@shared_task
def increment_view(user_id, movie_id):
    try:
        user = User.objects.get(pk=user_id)
        movie = Movie.objects.get(tmdb_id=movie_id)
    except ObjectDoesNotExist:
        return

    # Check if the user has already viewed the post
    if MovieView.objects.filter(user=user, movie=movie).exists():
        return

    # Create a new View object
    view = MovieView(user=user, movie=movie)
    view.save()

    # Update the like count of the post
    # post.views = View.objects.filter(post=post).count()
    # post.save()

@shared_task
def create_or_update_movie():

    items = []
    imdb_ids = []
    url = 'http://api.themoviedb.org/3/movie/popular?api_key=bceb6c0fefae8ee5a3cf9762ec780d63&page=1'
    api_url = "https://api.themoviedb.org/3/movie/"
    cinemagoer = Cinemagoer()

    response = requests.get(url).json()

    for item in response['results']:
        item_id = item.get('id')
        items.append(item_id)

    for tmdb_id in items:
        url = f"{api_url}{tmdb_id}/external_ids?api_key=bceb6c0fefae8ee5a3cf9762ec780d63"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(f"Data for tmdb-ID {tmdb_id}:")
            imdb_id = data.get('imdb_id')
            print(data.get('imdb_id'))

            imdb_id = imdb_id.replace('tt', '')
            movie = cinemagoer.get_movie(imdb_id)
            # print(movie.get('title'))
            # print(movie.current_info)
            # print(movie.infoset2keys)

            # print('plot')
            # print(movie.get('plot'))
            title = movie.get('title')
            plot = movie.get('plot')
            # imdb_ids.append(imdb_id)

            movie = Movie(
                tmdb_id=tmdb_id,
                title=title,
                description=plot,
                # poster=poster,
                imdb_id=imdb_id
            )
            movie.save()
        else:
            print(f"Error retrieving data for ID {id}: {response.status_code}")

# ChatGPT
# @shared_task
# def update_model_field(model_instance_id, new_value):
#     try:
#         obj = Movie.objects.get(id=model_instance_id)
#         obj.field_to_update = new_value
#         obj.save()
#     except ObjectDoesNotExist:
#         # Handle the case where the object is not found
#         pass
