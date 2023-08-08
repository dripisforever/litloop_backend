# from django.shortcuts import render
# from rest_framework import permissions, status
# from rest_framework.exceptions import PermissionDenied
# from rest_framework.parsers import (
#     FileUploadParser,
#     FormParser,
#     JSONParser,
#     MultiPartParser,
# )
# from rest_framework.response import Response
# from rest_framework.settings import api_settings
# from rest_framework.views import APIView
#
# # Create your views here.
# class CommentList(APIView):
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorizedToAdd)
#     parser_classes = (JSONParser, MultiPartParser, FormParser, FileUploadParser)
#
#     def get(self, request, format=None):
#         pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
#         paginator = pagination_class()
#         comments = Comment.objects.filter()
#         comments = comments.prefetch_related("user")
#         comments = comments.prefetch_related("media")
#         params = self.request.query_params
#         if "author" in params:
#             author_param = params["author"].strip()
#             user_queryset = User.objects.all()
#             user = get_object_or_404(user_queryset, username=author_param)
#             comments = comments.filter(user=user)
#
#         page = paginator.paginate_queryset(comments, request)
#
#         serializer = CommentSerializer(page, many=True, context={"request": request})
#         return paginator.get_paginated_response(serializer.data)
#
#
# class CommentDetail(APIView):
#     """Comments related views
#     Listings of comments for a media (GET)
#     Create comment (POST)
#     Delete comment (DELETE)
#     """
#
#     permission_classes = (IsAuthorizedToAdd,)
#     parser_classes = (JSONParser, MultiPartParser, FormParser, FileUploadParser)
#
#     def get_object(self, friendly_token):
#         try:
#             media = Media.objects.select_related("user").get(friendly_token=friendly_token)
#             self.check_object_permissions(self.request, media)
#             if media.state == "private" and self.request.user != media.user:
#                 return Response({"detail": "media is private"}, status=status.HTTP_400_BAD_REQUEST)
#             return media
#         except PermissionDenied:
#             return Response({"detail": "bad permissions"}, status=status.HTTP_400_BAD_REQUEST)
#         except BaseException:
#             return Response(
#                 {"detail": "media file does not exist"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#
#     def get(self, request, friendly_token):
#         # list comments for a media
#         media = self.get_object(friendly_token)
#         if isinstance(media, Response):
#             return media
#         comments = media.comments.filter().prefetch_related("user")
#         pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
#         paginator = pagination_class()
#         page = paginator.paginate_queryset(comments, request)
#         serializer = CommentSerializer(page, many=True, context={"request": request})
#         return paginator.get_paginated_response(serializer.data)
#
#
#     def delete(self, request, friendly_token, uid=None):
#         """Delete a comment
#         Administrators, MediaCMS editors and managers,
#         media owner, and comment owners, can delete a comment
#         """
#         if uid:
#             try:
#                 comment = Comment.objects.get(uid=uid)
#             except BaseException:
#                 return Response(
#                     {"detail": "comment does not exist"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             if (comment.user == self.request.user) or comment.media.user == self.request.user or is_mediacms_editor(self.request.user):
#                 comment.delete()
#             else:
#                 return Response({"detail": "bad permissions"}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#     def post(self, request, friendly_token):
#         """Create a comment"""
#         media = self.get_object(friendly_token)
#         if isinstance(media, Response):
#             return media
#
#         if not media.enable_comments:
#             return Response(
#                 {"detail": "comments not allowed here"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         serializer = CommentSerializer(data=request.data, context={"request": request})
#         if serializer.is_valid():
#             serializer.save(user=request.user, media=media)
#             if request.user != media.user:
#                 notify_user_on_comment(friendly_token=media.friendly_token)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
