from pydeezer import Deezer
from pydeezer import Downloader
from pydeezer.constants import track_formats

arl = "ed7b984780713c28f42d81256f7023120f1e36baae8b2e4876195d258994c7dade471bd0d69e09382b9333d600e5534d73a2f2a8599c25d74c03ef9fd16f652f0280f95724991939cb4863204857a978386952245f66f15c91d0eefd8f415fae"
deezer = Deezer(arl=arl)
# user_info = deezer.user

download_dir = "/Users/driptamine/Desktop/DEEZER"

# track_id = "547653622"
track_id = "856558962"
track = deezer.get_track(track_id)
# search_data = deezer.search_tracks("скриптонит")

# list_of_ids = []
# for track_data in search_data:
#     track_id = track_data['id']
#     list_of_ids.append(track_id)

# track is now a dict with a key of info, download, tags, and get_tag
# info and tags are dict
# track_info = track["info"]

# j = json.dumps(track_info, ensure_ascii=False).encode('utf8').decode()

# tags_separated_by_comma = track["tags"]
# download and get_tag are partial functions
track["download"](download_dir, quality=track_formats.MP3_128) # this will download the file, default file name is Filename.[mp3 or flac]




# tags_separated_by_semicolon = track["get_tag"](separator="; ") # this will return a dictionary similar to track["tags"] but this will override the default separator
#
# artist_id = "53859305"
# artist = deezer.get_artist(artist_id)
#
# album_id = "39949511"
# album = deezer.get_album(album_id) # returns a dict containing data about the album
#
# playlist_id = "1370794195"
# playlist = deezer.get_playlist(playlist_id) # returns a dict containing data about the playlist

# Multithreaded Downloader

# list_of_id = ["572537082",
#               "921278352",
#               "927432162",
#               "547653622"]
#
# downloader = Downloader(deezer, list_of_ids, download_dir,
#                         quality=track_formats.MP3_320, concurrent_downloads=2)
# downloader.start()
