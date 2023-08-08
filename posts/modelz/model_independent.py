# reference: https://github.com/Fedor-Skorokhodov/Blog_Django/blob/21fe83f46de9662913736002313b969da3497e11/post/models.py

from django.db import models
from home.models import UserModel


class Post(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    # media = models.ManyToManyField(Media, through="postmedia")
    videos = models.ManyToManyField(Video, through="PostVideo")
    tracks = models.ManyToManyField(Track, through="PostTrack")
    photos = models.ManyToManyField(Photo, through="PostPhoto")
    gallery = models.ManyToManyField(Gallery, through="PostGallery")
    playlists = models.ManyToManyField(Playlist, through="PostPlaylist")

class Photo(models.Model):
    image = models.ImageField(upload_to='post/images')


class Video(models.Model):
    video = models.FileField(upload_to='post/videos')


class Track(models.Model):
    artists = models.ManyToManyField(Artist, through="TrackArtist")

    audio = models.FileField(upload_to='post/tracks')

class Gallery(models.Model):

    elements = models.ManyToManyField(Element, through="GalleryElement")

class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    answer_to = models.ForeignKey('self', null=True, default=None, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='comments/images', null=True, default=None)
    video = models.FileField(upload_to='comments/videos', null=True, default=None)
    track = models.FileField(upload_to='comments/tracks', null=True, default=None)
