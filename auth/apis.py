#ref https://github.com/HackSoftware/Django-React-GoogleOauth2-Example/blob/main/server/auth/apis.py

from urllib.parse import urlencode

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework_jwt.views import ObtainJSONWebTokenView

from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.core.serializers import serialize
import json

# from api.mixins import ApiErrorsMixin, PublicApiMixin, ApiAuthMixin

from users.services import user_record_login, user_change_secret_key, user_get_or_create

from .services import (
    jwt_login,
    google_get_access_token,
    twitch_get_access_token,
    google_get_user_info,
    twitch_get_user_info
)


def redirect_to_google_oauth_url(self):
    url = "https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount"
    response_type = "code"
    client_id = ""
    redirect_uri = "http://localhost:8000/auth/google/callback"
    prompt = "select_account"
    access_type = "offline"
    scope = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]
    oauth_redirect_url = f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&prompt={prompt}&access_type={access_type}&scope={scope}'
    return redirect(oauth_redirect_url)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    redirect_uri = "http://localhost:3001/auth/spotify/callback"
    access_token = spotify_get_access_token(code=code, redirect_uri=redirect_uri)

    user_data = google_get_user_info(access_token=access_token)

    profile_data = {
        'email': user_data['email'],
        'avatar': user_data['picture'],
        'username': user_data['given_name']

    }
    user, _ = user_get_or_create(**profile_data)

    return user


class GoogleLoginApiOld(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def put(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        # login_url = f'{settings.BASE_FRONTEND_URL}/login'
        #
        # if error or not code:
        #     params = urlencode({'error': error})
        #     return redirect(f'{login_url}?{params}')

        redirect_uri = "http://localhost:8000/auth/google/callback"
        # redirect_uri = "http://localhost:3000/auth/google/callback"
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        profile_data = {
            'email': user_data['email'],
            'avatar': user_data['picture'],
            'username': user_data['given_name']
        }

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**profile_data)

        # REDIRECT TO REACT APP
        # client_callback_url = "http://localhost:3001/auth/callback"
        client_callback_url = "http://localhost:3001/auth/callback?token="+access_token

        # response = redirect(client_callback_url)
        response = client_callback_url
        response = jwt_login(response=response, user=user)
        last = redirect(response)
        return last
        # return response


        # BRAINSTORM
        # response = redirect('http://localhost:3001/auth/callback')
        # response['Set-Cookie'] = 'Test'
        # del response['Test']
        # response['Authorization'] = 'Bearer '+ jwt
        #
        # return response


class GoogleLoginApi(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def put(self, request, *args, **kwargs):
        code = request.data.get('code', False)

        redirect_uri = "http://localhost:3001/auth/google/callback"
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        # user_data = twitch_get_user_info(access_token=access_token)
        #
        # profile_data = {
        #     'email': user_data['email'],
        #     'avatar': user_data['picture'],
        #     'username': user_data['given_name']
        # }
        #
        # # We use get-or-create logic here for the sake of the example.
        # # We don't have a sign-up flow.
        # user, _ = user_get_or_create(**profile_data)

        return Response(access_token)

class TwitchLoginApi(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def put(self, request, *args, **kwargs):
        code = request.data.get('code', False)

        redirect_uri = "http://localhost:3001/auth/twitch/callback"
        access_token = twitch_get_access_token(code=code, redirect_uri=redirect_uri)

        # user_data = twitch_get_user_info(access_token=access_token)
        #
        # profile_data = {
        #     'email': user_data['email'],
        #     'avatar': user_data['picture'],
        #     'username': user_data['given_name']
        # }
        #
        # # We use get-or-create logic here for the sake of the example.
        # # We don't have a sign-up flow.
        # user, _ = user_get_or_create(**profile_data)

        return Response(access_token)



# class SpotifyLoginApi(PublicApiMixin, ApiErrorsMixin, APIView):
#     class InputSerializer(serializers.Serializer):
#         code = serializers.CharField(required=False)
#         error = serializers.CharField(required=False)
#
#     def get(self, request, *args, **kwargs):
#         input_serializer = self.InputSerializer(data=request.GET)
#         input_serializer.is_valid(raise_exception=True)
#
#         validated_data = input_serializer.validated_data
#
#         code = validated_data.get('code')
#         error = validated_data.get('error')
#
#         login_url = f'{settings.BASE_FRONTEND_URL}/login'
#
#         if error or not code:
#             params = urlencode({'error': error})
#             return redirect(f'{login_url}?{params}')
#
#         # domain = "localhost:8000/users/spotify/callback"
#         domain = "http://127.0.0.1:8000/users/spotify/callback"
#         # api_uri = reverse('api:v1:auth:login-with-google')
#         # redirect_uri = f'{domain}{api_uri}'
#
#         access_token = spotify_get_access_token(code=code, redirect_uri=domain)
#
#         user_data = spotify_get_user_info(access_token=access_token)
#
#         profile_data = {
#             'uri': user_data['id'],
#             'name': user_data.get('display_name', ''),
#             'image': user_data['images'][0].url
#         }
#
#         # We use get-or-create logic here for the sake of the example.
#         # We don't have a sign-up flow.
#         user, _ = user_get_or_create(**profile_data)
#
#         # REDIRECT TO REACT APP
#         response = redirect("localhost:3000/")
#         response = jwt_login(response=response, user=user)
#
#         return response


# class LogoutApi(ApiAuthMixin, ApiErrorsMixin, APIView):
#     def post(self, request):
#         """
#         Logs out user by removing JWT cookie header.
#         """
#         user_change_secret_key(user=request.user)
#
#         response = Response(status=status.HTTP_202_ACCEPTED)
#         response.delete_cookie(settings.JWT_AUTH['JWT_AUTH_COOKIE'])
#
#         return response


# def redirect_to_apple_oauth_url(self):
#     https://appleid.apple.com/auth/authorize?
#     client_id=com.zhiliaoapp.musically.siwa-web&
#     redirect_uri=https%3A%2F%2Fwww.tiktok.com%2Foauth&
#     response_type=code%20id_token&
#     state=c30c764b3gASoVCgoVPZIDRjYWE0OWIyYmFlYzlhZWRhYmNlZDM0ZTE1ZjhlNTg1oU7ZJWh0dHBzOi8vd3d3LnRpa3Rvay5jb20vZm9yeW91P2xhbmc9ZW6hVgGhSQChRAChQdEFs6FNAKFIrnd3dy50aWt0b2suY29toVIColBM0QK0pkFDVElPTqpsb2dpbl9vbmx5oUy8aHR0cHM6Ly93d3cudGlrdG9rLmNvbS9sb2dpbqFU2SAzNWYzYmI4NzdhZDBmODkzMTIzMTJlNzA4OTZmMTE3ZKFXAKFGAKJTQQChVcI%253D&
#     scope=name%20email&
#     response_mode=web_message&
#     frame_id=7981049f-77f9-4fbd-a4ce-d369a7bb2101&
#     m=11&
#     v=1.5.4
#
#     url = "https://appleid.apple.com/auth/authorize"
#     response_type =
#     client_id =
#     redirect_uri =
#     prompt =
#     access_type =
#     oauth_redirect_url = f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&prompt={prompt}&access_type={access_type}&scope={scope}'
#     return redirect(oauth_redirect_url)



# def redirect_to_spotify_oauth_url(self):
#     https://accounts.spotify.com/authorize?
#     client_id=8b5a14d8cbc64d0995afc80ee2722fe3&
#     redirect_uri=https%3A%2F%2Fartist-explorer.glitch.me%2Fcallback.html&
#     response_type=token&
#     scope=playlist-read-private%20playlist-modify-public%20playlist-modify-private
#
#     url = "https://accounts.spotify.com/authorize"
#     response_type =
#     client_id =
#     redirect_uri =
#     prompt =
#     access_type =
#     oauth_redirect_url = f'{url}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&prompt={prompt}&access_type={access_type}&scope={scope}'
#     return redirect(oauth_redirect_url)


# def oauth_google_provider():
#     from oauthlib.oauth2 import WebApplicationClient
#
#     client_id = 'xxxxx'
#     client = WebApplicationClient(client_id)
#
#     authorization_url = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount'
#     scope = [
#         'https://www.googleapis.com/auth/userinfo.email',
#         'https://www.googleapis.com/auth/userinfo.profile'
#     ]
#     url = client.prepare_request_uri(
#       authorization_url,
#       redirect_uri = 'http://localhost:8000/oauth/callback',
#       scope = scope,
#       state = 'D8VAo311AAl_49LAtM51HA'
#     )
#     return HttpResponseRedirect(url)

#
# class GoogleTestApi(APIView):
#     class InputSerializer(serializers.Serializer):
#         code = serializers.CharField(required=False)
#         error = serializers.CharField(required=False)
#
#     def get(self, request, *args, **kwargs):
#         input_serializer = self.InputSerializer(data=request.GET)
#         input_serializer.is_valid(raise_exception=True)
#
#         validated_data = input_serializer.validated_data
#
#         code = validated_data.get('code')
#         error = validated_data.get('error')
#
#         redirect_uri = "http://localhost:8000/auth/google/callback"
#         access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
#
#         user_data = google_get_user_info(access_token=access_token)
#
#         profile_data = {
#             'email': user_data['email'],
#             'avatar': user_data['picture'],
#             'username': user_data['given_name']
#
#         }
#         user, _ = user_get_or_create(**profile_data)
#         # str_data = serialize('json', user) # Or you don't need to provide the `cls` here because by default cls is DjangoJSONEncoder
#         #
#         # data = json.loads(str_data)
#         # return Response(data)
#         return user
#         # return Response(user)
