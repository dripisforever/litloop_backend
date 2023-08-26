from django.urls import re_path, include, path

re_path(r'^celery-progress/', include('celery_progress.urls'))


# this.express.use('/', IndexRouter)
# this.express.use('/status', WorkflowStatusRouter)
# this.express.use('/test', router)
# this.router.get('/', this.renderStatus.bind(this))
# this.router.get('/poll/:statusURI', this.pollStatus.bind(this))

from videos.views import (
    # PostDetailAPIView,
    # PostListAPIView,
    # PostSearchAPIView,
    TrackDetailAPIView,
    TrackGetOrCreateAPIView,
    SearchTrackAPIView,
    TrackListAPIView,
    TrackPaginationAPIView,
)

from likes.api.views import (
    LikeListAPIView,
    PostLikedByList,
    LikedCountAPIView,
    LikeToggleView,
    LikedIDsAPIView
)


urlpatterns = [
    path('/upload', IndexRouter.as_view(), name="register"),
    path('/status', WorkflowStatusRouter.as_view(), name="login"),
    path('/status/poll/:statusURI', pollStatus.as_view(), name="login"),

    path('', TrackListAPIView.as_view(), name="posts"),
    # path('', TrackPaginationAPIView.as_view(), name="posts"),
    path('search', SearchTrackAPIView.as_view(), name="search"),
    # path('<int:id>', PostDetailAPIView.as_view(), name="post"),

    path('<int:id>/like/', LikeToggleView.as_view(), name="post"),
    path('<int:id>/likers/', PostLikedByList.as_view(), name="post"),
    path('<str:video_uri>/upd', TrackGetOrCreateAPIView.as_view(), name="track_detail"),
    path('<str:video_uri>/', TrackDetailAPIView.as_view(), name="track_detail"),
]


# from django.urls import path, include
#
# from . import views
#
# urlpatterns = [
#     path('', views.VideoListView.as_view(), name="video_index"),
#     path('search/<collection>/', views.VideoListView.as_view(), name="video_index"),
#     path('videos/<slug:slug>/', include([
#         path('play/', views.VideoPlayerView.as_view(), name="video_player"),
#         path('edit/', views.EditVideoView.as_view(), name="edit_video"),
#         path('delete/', views.DeleteVideoView.as_view(), name="delete_video"),
#         path('download/', views.DownloadVideoView.as_view(), name="download_video"),
#         path('thumbnail/', views.GetVideoThumbnailView.as_view(), name="get_thumbnail"),
#         path('gif/', views.GetVideoGifPreviewView.as_view(), name="get_gif_preview"),
#         path('track_playback/', views.TrackPlaybackView.as_view(), name="track_playback"),
#         path('master_playlist/', include([
#             path('', views.GetMasterPlaylistView.as_view(), name="get_master_playlist"),
#             path('<int:variant>.m3u8', views.GetVariantPlaylistView.as_view(), name="get_variant_playlist"),
#             path('<int:variant>.m4s', views.GetVariantVideoView.as_view(), name="get_video"),
#         ])),
#     ])),
#     path('upload/', views.VideoFormView.as_view(), name="video_form"),
#     path('uploads/', views.UserUploadsView.as_view(), name="user_uploads"),
#     path('collection/', include([
#         path('edit/', views.EditVideoCollectionView.as_view(), name='collection_edit'),
#         path('<slug:slug>/edit/', views.EditVideoCollectionView.as_view(), name='collection_edit'),
#     ])),
#     path('api/autocomplete/', include([
#         path(
#             'collection/',
#             views.CollectionAutocomplete.as_view(create_field='title'),
#             name='autocomplete_collection'
#         ),
#     ])),
#     path('video_file_upload/', include([
#         path('', views.VideoChunkedUploadView.as_view(), name='video_chunked_upload'),
#         path('complete/', views.VideoChunkedUploadCompleteView.as_view(), name='video_chunked_upload_complete'),
#     ])),
# ]
#
#
#
