import requests
from imdb import Cinemagoer

items = []
imdb_ids = []
url = 'http://api.themoviedb.org/3/movie/popular?api_key=bceb6c0fefae8ee5a3cf9762ec780d63&page=1'
api_url = "https://api.themoviedb.org/3/movie/"
cinemagoer = Cinemagoer()

response = requests.get(url).json()

for item in response['results']:
    item_id = item.get('id')
    items.append(item_id)

for id in items:
    url = f"{api_url}{id}/external_ids?api_key=bceb6c0fefae8ee5a3cf9762ec780d63"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(f"Data for tmdb-ID {id}:")
        imdb_id = data.get('imdb_id')
        print(data.get('imdb_id'))

        imdb_id = imdb_id.replace('tt', '')
        movie = cinemagoer.get_movie(imdb_id)
        print(movie.get('title'))
        # print(movie.current_info)
        # print(movie.infoset2keys)

        # print('plot')
        # print(movie.get('plot'))
        # imdb_ids.append(imdb_id)
    else:
        print(f"Error retrieving data for ID {id}: {response.status_code}")
