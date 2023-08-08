import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from albums.models import Album


SPOTIPY_CLIENT_ID = "c57cfe40c3a640449c4766ee61ec9d59"

SPOTIPY_CLIENT_SECRET = "8c5ae0b0d9df47c8bae2804fe8e03cfa"

# sp = spotipy.Spotify(
#     client_credentials_manager=SpotifyClientCredentials(
#         client_id=SPOTIPY_CLIENT_ID,
#         client_secret=SPOTIPY_CLIENT_SECRET
#     )
# )

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET))

# album_uri = "4NZWRpoMuXaHU7csTjWdB5"
# album_uri = "1e97vaQCuuZH9515xaj2cd"
# album_info = sp.album(album_uri)

album_info = sp.album("1e97vaQCuuZH9515xaj2cd")


Album.create(**album_info)


# artist = Artist.objects.get(
#     artist_uri=kwargs['artists']['uri']
#
# )
# album.artists.add(artist)

# for data in album_info['tracks']['items']:
#     name = data['name']
#     name


# json_to_dict = json.dumps(album_info)
# json_data = dict(json_to_dict)
# json_data = json_to_dict

# for album_data in json_data:
# for album_data in album_info:
#     data = Album.create(**album_data)

# data = Album.create(**album_data)




# str_to_json = json.dumps(album_info)

# convert_str_to_json = json.loads(str_to_json)



# album = cls.objects.get_or_create(
#     # artist_id = kwargs['artists']['id'],
#     album_id = kwargs['id'],
#     name = kwargs['name'],
#     href = current_site + "album/" + kwargs['id'] + "/",
#
#     # defaults = {
#     #     'artist_id': artist.artist_id,
#     #     'album_id': kwargs['id'],
#     #     'name': kwargs['name'],
#     #     'href': current_site + "album/" + kwargs['id'] + "/",
#     # }
# )
