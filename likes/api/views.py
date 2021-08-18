from rest_framework import status
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from likes.api.pagination import get_pagination_class
from likes.api.serializers import (
    LikeListSerializer,
    LikeToggleSerializer,
    LikeContentTypeSerializer
)
from likes.models import Like
from posts.models import Post
from likes.selectors import get_liked_object_ids, get_users_who_liked_object, get_user_likes
from likes.services import get_user_likes_count

from posts.serializers import PostSerializer

__all__ = (
    'LikedCountAPIView',
    'LikedIDsAPIView',
    'LikeToggleView',
    'LikeListAPIView',
    'LikersListAPIView',
)


class LikeToggleView(CreateAPIView):
    """
    post:
    API View to like-unlike given object by authenticated user.\n
    Possible payload:\n
        {
            "type": "app_label.model",  // object's content type's natural key joined string
            "id": 1  // object's primary key
        }
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeToggleSerializer
    # serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        data['is_liked'] = getattr(serializer, 'is_liked', True)
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )
        
class LikeAlbumToggleView(CreateAPIView):
    """
    post:
    API View to like-unlike given object by authenticated user.\n
    Possible payload:\n
        {
            "type": "app_label.model",  // object's content type's natural key joined string
            "id": 1  // object's primary key
        }
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeToggleSerializer
    # serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        data['is_liked'] = getattr(serializer, 'is_liked', True)
        # album = AlbumSerializer()
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )


# class LikersListAPIView(ListAPIView):
#     permission_classes = (AllowAny, )
#
#     def get(self, request, *args, **kwargs):
#         serializer = LikeContentTypeSerializer(data=request.GET)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(
#             data={
#                 'ids': get_users_who_liked_object(
#                     user=self.request.user,
#                     content_type=serializer.validated_data.get(
#                         'type'
#                     )
#                 )
#             }
#         )


class LikedCountAPIView(APIView):
    """
    API View to return count of likes for authenticated user.
    """
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        serializer = LikeContentTypeSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)

        return Response(
            data={
                'count': get_user_likes_count(
                    user=request.user,
                    content_type=(
                        serializer.validated_data.get(
                            'type'
                        )
                    )
                )
            }
        )


class LikedIDsAPIView(APIView):
    """
    User liked ids:
    API View to return liked objects ids for a given user.
    """
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        serializer = LikeContentTypeSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        post_serializer = PostSerializer
        return Response(
            data={
                'ids': get_liked_object_ids(
                    user=self.request.user,
                    content_type=serializer.validated_data.get(
                        'type'
                    )
                ),
                # 'posts': Post.objects.filter(likes__user=self.request.user)
                # 'posts': get_user_likes(user=self.request.user, content_type=post_serializer.validated_data.get('type'))
            }
        )
        #


class PostLikedByList(ListAPIView):
    # queryset = Post.objects.all()
    # serializer_class = PostSerializer


    # permission_classes = (IsAuthenticated,)
    # lookup_field = 'id'
    # def perform_create(self, serializer):
    #     serializer.save(publisher=self.request.user)

    # def get_queryset(self):

    def get(self, request, id):
        """
        /posts/:id/likes/
        """

        post_id = Post.objects.get(id=id).likes.all()
        serializer = LikeListSerializer(post_id, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeListAPIView(ListAPIView):
    """
    List API View to return all likes for authenticated user.
    Possible payload:\n
        {
            "type": "app_label.model",  // object's content type's natural key joined string
            "id": 1  // object's primary key
        }
    """
    pagination_class = get_pagination_class()
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeListSerializer
    queryset = Like.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = (
        'content_type__model',
    )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                user=self.request.user
            )
            .select_related('user')
            .distinct()
        )
