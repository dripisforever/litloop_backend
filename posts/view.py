from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from posts.models import Post


class PostLikeAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request) -> Response:

        user = request.user
        post_id = request.POST.get('post_id', False)

        if not post_id:
            return Response(
                {'error': 'post_id required'}, status=status.HTTP_400_BAD_REQUEST
            )

        post = get_object_or_404(Post, id=post_id)
        try:
            if (
                not post.user.private
                or post.user == user
                or post.id
                in Post.objects.filter(
                    user_id__in=user.following.values_list('id', flat=True)
                ).values_list('id', flat=True)
            ):
                post.votes.up(user.id)
            else:
                return Response({'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'like': 'existed'}, status=status.HTTP_200_OK)
        else:
            return Response({'like': 'created'}, status=status.HTTP_201_CREATED)


class LikePostAPIView(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
    return Response({}, status=200)


class LikeToggle(APIView):

    pass
