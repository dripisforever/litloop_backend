from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse

from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.generics import (ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, UpdateAPIView, )
from rest_framework.views import APIView
from rest_framework.decorators import action


from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from posts.models import Post
from posts.serializers import PostSerializer
from .utils import Util
from .renderers import UserRenderer
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, UserSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import jwt
import json

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        # user_token = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        # current_site = request.get_host()
        # current_site = 'flipdab.com/'
        # current_site = 'localhost:8000/'
        relative_link = reverse('email-verify')

        url_with_token = 'http://' + current_site + relative_link+'?token=' + str(token)
        email_body = 'Hi ' + user.username + ' Use link below to verify your email: \n' + url_with_token

        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject':'Verify your email',
        }

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)

    # def perform_create(self, serializer):
        # return serializer.save(author=self.request.user)

    # def get_queryset(self):
        # return self.queryset.filter(author=self.request.user)


class CurrentUserView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    def get(self, request):
        context = {'request':request}
        serializer = UserSerializer(request.user, context=context)
        # serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    # def me(self, request, *args, **kwargs):
    #     # assumes the user is authenticated, handle this according your needs
    #     user_id = request.user.id
    #     # return self.retrieve(request, user_id)


# REFERENCE https://www.youtube.com/watch?utm_source=pocket_saves&v=PUzgZrS_piQ
class CurrentUserViewAPI(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

class UpdateCurrentUserView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    def put(self, request):
        context = {'request':request}
        serializer = UserSerializer(request.user, context=context)
        # serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
class UserDetailAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = 'username'

    # def get_queryset(self):
        # return self.queryset.filter(author=self.request.user)
    # def patch(self, request, username):
    #     testmodel_object = self.get_object(self, username)
    #     serializer = UserSerializer(testmodel_object, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(code=201, data=serializer.data)
    #     return JsonResponse(code=400, data="wrong parameters")


class UserDetailByIdAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = 'id'

    # def get_queryset(self):
        # return self.queryset.filter(author=self.request.user)

    def patch(self, request, id):
        # testmodel_object = self.get_object(self, id)
        testmodel_object = User.objects.get(id=id)
        serializer = UserSerializer(testmodel_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(code=201, data=serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # return JsonResponse(code=400, data="wrong parameters")

    def get(self, request, id):
        """
        /users/:id/
        """
        user_id = User.objects.get(id=id)
        # track_id = Track.objects.get_or_create(id=id)
        user_posts = Post.objects.filter(author=user_id)
        serializer = PostSerializer(user_posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return self.queryset.filter(likes__user=user_id)


class UserPostsList(ListAPIView):
    # queryset = Post.objects.all()
    # serializer_class = PostSerializer


    # permission_classes = (IsAuthenticated,)
    # lookup_field = 'id'
    # def perform_create(self, serializer):
    #     serializer.save(publisher=self.request.user)

    # def get_queryset(self):

    def get(self, request, id):
        """
        /users/:id/posts
        """
        user_id = User.objects.get(id=id)

        # track_id = Track.objects.get_or_create(id=id)
        user_posts = Post.objects.filter(author=user_id)

        # album_id = Album.objects.get(id=id)
        # album_tracks = Track.objects.filter(album=album_id)

        serializer = PostSerializer(user_posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return self.queryset.filter(likes__user=user_id)


class UserLikedPostsList(ListAPIView):
    # queryset = Post.objects.all()
    # serializer_class = PostSerializer


    # permission_classes = (IsAuthenticated,)
    # lookup_field = 'id'
    # def perform_create(self, serializer):
    #     serializer.save(publisher=self.request.user)

    # def get_queryset(self):

    def get(self, request, id):
        """
        /users/:id/likes/
        """
        user_id = User.objects.get(id=id)
        # track_id = Track.objects.get_or_create(id=id)
        user_liked_posts = Post.objects.filter(likes__user=user_id)
        serializer = PostSerializer(user_liked_posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return self.queryset.filter(likes__user=user_id)

# class UserAvatarListAPIView(APIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     lookup_field = 'username'

#     def patch(self, request, username):
#         testmodel_object = self.get_object(self, username)
#         serializer = UserSerializer(testmodel_object, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(code=201, data=serializer.data)
#         return JsonResponse(code=400, data="wrong parameters")


# class CurrentUserSavedTracks(ListAPIView):
#     import spotipy
#     from spotipy.oauth2 import SpotifyOAuth
#
#     scope = "user-library-read"
#
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
#
#     results = sp.current_user_saved_tracks()
#     for idx, item in enumerate(results['items']):
#         track = item['track']
#         print(idx, track['artists'][0]['name'], " – ", track['name'])
