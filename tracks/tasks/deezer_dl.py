from __future__ import absolute_import, unicode_literals
from celery import shared_task

from pydeezer import Deezer
from pydeezer import Downloader
from pydeezer.constants import track_formats

arl = "ed7b984780713c28f42d81256f7023120f1e36baae8b2e4876195d258994c7dade471bd0d69e09382b9333d600e5534d73a2f2a8599c25d74c03ef9fd16f652f0280f95724991939cb4863204857a978386952245f66f15c91d0eefd8f415fae"
deezer = Deezer(arl=arl)

download_dir = "/Users/driptamine/Desktop/DEEZER"

# track_id = "547653622"
track_id = "856558962"
track = deezer.get_track(track_id)
track["download"](download_dir, quality=track_formats.MP3_128) # this will download the file, default file name is Filename.[mp3 or flac]


# Multithreaded Downloader

list_of_id = [
    "572537082",
    "921278352",
    "927432162",
    "547653622"
]

downloader = Downloader(deezer, list_of_ids, download_dir, quality=track_formats.MP3_320, concurrent_downloads=2)
downloader.start()

@shared_task
def search_and_download(self, query):
    # search_data = deezer.search_tracks("скриптонит")
    search_data = deezer.search_tracks(query, limit=10)

    list_of_ids = []
    for track_data in search_data:
        track_id = track_data['id']
        list_of_ids.append(track_id)

    downloader = Downloader(deezer, list_of_ids, download_dir, quality=track_formats.MP3_320, concurrent_downloads=2)
    downloader.start()


def sleep_rate_download():
    pass
