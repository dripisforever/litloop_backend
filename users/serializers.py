from rest_framework import serializers
from users.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
# from posts.serializers import PostsSerializer

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'password',
            'avatar',
        ]

    def validate(self,attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):

    token = serializers.CharField(max_length=555)

    class Meta:
        model  = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3,)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    # avatar = serializers.FileField()
    # tokens = serializers.CharField(max_length=68, read_only=True)
    access_token = serializers.CharField(max_length=68, read_only=True)
    refresh_token = serializers.CharField(max_length=68, read_only=True)
    # tokens = serializers.JSONField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'avatar',
            'username',
            'access_token',
            'refresh_token'
        ]


    def validate(self, attrs):
        email = attrs.get('email', '')
        # username = attrs.get('username', '')
        password = attrs.get('password', '')

        # if User.objects.filter(username=username).exists:
        #     user = auth.authenticate(username=username, password=password)
        # else:
        #     user = auth.authenticate(email=username, password)

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')


        return {
            'id': user.id,
            'email': user.email,
            'avatar': user.avatar,
            'username': user.username,
            'access_token': user.access_token,
            'refresh_token': user.refresh_token
        }


        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3,)
    # password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    # posts = PostsSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            # 'uuid',
            'avatar',
            'username',
            'email',
            'created_at',
            'updated_at',
            'posts',
            'posts_count',
            'likes_count',
        ]
    # class Meta:
    #     model = User
    #     fields = '__all__'
