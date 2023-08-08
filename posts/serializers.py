from rest_framework import serializers
from posts.models import Post
from users.serializers import UserSerializer
from likes import services as likes_services


class PostSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    author = UserSerializer()
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            # 'uuid',
            'author',
            # 'user'
            'caption',
            'image',
            'is_liked',
            'likes_count',
            'views',
            'views_count',
            'total_likes',
            'created_at',
            'updated_at',
        ]

    def get_is_liked(self, obj):

        # user = self.context.get('request').user
        user = self.context['request'].user
        return likes_services.is_fan(obj, user)

    def get_total_likes(self, obj):
        return likes_services.get_object_likes_count(obj)


class PostsSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    # author = UserSerializer()
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'caption',
            'image',
            'is_liked',
            'likes_count',
            'total_likes',
            'created_at',
            'updated_at',
        ]

    def get_is_liked(self, obj):

        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def get_total_likes(self, obj):
        return likes_services.get_object_likes_count(obj)


    # def to_representation(self, instance):

    #     result =

class PostCreateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Post
        fields = [
            'id',
            # 'author',
            'caption',
            'image',
            'created_at',
            'updated_at',

        ]


# class PostLikersSerializer(serializers.ModelSerializer):
#     pass
