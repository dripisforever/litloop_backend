from django.urls import path
from .views import (
    UserView,
    RegisterView,
    VerifyEmail,
    LoginAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserDetailByIdAPIView,
    # UserAvatarListAPIView,
    CurrentUserView,
    CurrentUserViewAPI,
    UserLikedPostsList,
    UserPostsList,
    # UserLikeListAPIView
)

from likes.api.views import (
    LikedIDsAPIView,
    LikedCountAPIView,
    LikeListAPIView,
    # LikePageView
)

# from posts.views import


from django.urls import path
from .views import *


urlpatterns = [


    # USERS ENDPOINTS
    path('signup/', RegisterView.as_view(), name="register"),
    path('signin/', LoginAPIView.as_view(), name="login"),
    path('email_verify/', VerifyEmail.as_view(), name="email-verify"),
    path('list/', UserListAPIView.as_view(), name="users"),
    path('<int:id>/', UserDetailByIdAPIView.as_view(), name="user_detail_by_id"),
    path('me/', CurrentUserView.as_view(), name="current_user"),
    path('current_user/', CurrentUserViewAPI.as_view(), name="current_user_v2"),
    path('<int:id>/avatar/', UserView.as_view(), name="user_avatar"),

    path('twitch/<int:id>/update/', UserView.as_view(), name="twitch_user"),
    path('twitch/update/', UpdateCurrentUserView.as_view(), name="twitch_user"),

    path('<str:username>/', UserDetailAPIView.as_view(), name="user_detail"),

    # path('<str:username>/likes/', LikeListAPIView.as_view(), name="user_likes"),
    # path('<int:id>/likes/', LikedIDsAPIView.as_view(), name="user_likes"),
    # path('<int:id>/likes/', UserLikeListAPIView.as_view(), name="user_likes"),
    path('<int:id>/likes/', UserLikedPostsList.as_view(), name="user_likes"),
    path('<int:id>/posts/', UserPostsList.as_view(), name="user_likes"),
    # path('<int:id>/likes/album/', UserLikedPostsList.as_view(), name="user_likes"),
    # path('<int:id>/likes/', LikePageView.as_view(), name="user_likes"),
    # path('<int:id>/likes/', LikeListAPIView.as_view(), name="user_likes"),
    # path('<str:username>/', UserAvatarListAPIView.as_view(), name="user_avatar"),
]



# https://dev.litloop.co/oauth/applications/new
# https://dev.litloop.co/oauth/applications/318262
