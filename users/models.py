from django.db import models
from django.contrib.auth.models import(AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
import json

class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        if not email:
            raise TypeError('Users must have an email address')
        elif not username:
            raise TypeError('Users must have an username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email = email,
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'media/user_avatar/id{0}/{1}'.format(instance.id, filename)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.FileField(upload_to=user_directory_path, default="")

    # likings = models.ManyToManyField("self", blank=True)
    # following = models.ManyToManyField("self", blank=True)
    # followers = models.ManyToManyField("self", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


    # def posts_count(self):
    #     return self.posts.all().count()
    def likes_count(self):
        return self.likes.count()

    def posts_count(self):
        return self.posts.count()
    # def tokens(self):
    #     refresh_token = RefreshToken.for_user(self)
        
    #     return {
    #         'refresh': str(refresh_token),
    #         'access': str(refresh_token.access_token),
    #     }

    def access_token(self):
        refresh_token = RefreshToken.for_user(self)
        
        return str(refresh_token.access_token)

    def refresh_token(self):
        refresh_token = RefreshToken.for_user(self)
        
        return str(refresh_token)