import json
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# import media.helpers as helpers

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
        # user.has_perm = True
        user.save(using=self._db)
        return user

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploaded_media/user_avatar/id{0}/{1}'.format(instance.id, filename)

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

    ## A user may have access to zero or more advertisers or publishers
    # advertisers = models.ManyToManyField(Advertiser, blank=True)
    # publishers = models.ManyToManyField(Publisher, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


    # def posts_count(self):
    #     return self.posts.all().count()
    def likes_count(self):
        return self.likes.count()

    def views_count(self):
        return self.viewed.count()

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


# class Channel(models.Model):
#     title = models.CharField(max_length=90, db_index=True)
#     description = models.TextField(blank=True, help_text="description")
#     user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, related_name="channels")
#     add_date = models.DateTimeField(auto_now_add=True, db_index=True)
#     subscribers = models.ManyToManyField(User, related_name="subscriptions", blank=True)
#     friendly_token = models.CharField(blank=True, max_length=12)
#     banner_logo = ProcessedImageField(
#         upload_to="userlogos/%Y/%m/%d",
#         processors=[ResizeToFill(900, 200)],
#         default="userlogos/banner.jpg",
#         format="JPEG",
#         options={"quality": 85},
#         blank=True,
#     )
#
#     def save(self, *args, **kwargs):
#         # strip_text_items = ["description", "title"]
#         # for item in strip_text_items:
#         #     setattr(self, item, strip_tags(getattr(self, item, None)))
#
#         if not self.friendly_token:
#             while True:
#                 friendly_token = helpers.produce_friendly_token()
#                 if not Channel.objects.filter(friendly_token=friendly_token):
#                     self.friendly_token = friendly_token
#                     break
#         super(Channel, self).save(*args, **kwargs)
#
#     def __str__(self):
#         return "{0} -{1}".format(self.user.username, self.title)
#
#     def get_absolute_url(self, edit=False):
#         if edit:
#             return reverse("edit_channel", kwargs={"friendly_token": self.friendly_token})
#         else:
#             return reverse("view_channel", kwargs={"friendly_token": self.friendly_token})
#
#     @property
#     def edit_url(self):
#         return self.get_absolute_url(edit=True)


@receiver(post_save, sender=User)
def post_user_create(sender, instance, created, **kwargs):
    # create a Channel object upon user creation, name it default
    if created:
        new = Channel.objects.create(title="default", user=instance)
        new.save()
        if settings.ADMINS_NOTIFICATIONS.get("NEW_USER", False):
            title = "[{}] - New user just registered".format(settings.PORTAL_NAME)
            msg = """
                User has just registered with email %s\n
                Visit user profile page at %s
            """ % (
                instance.email,
                settings.SSL_FRONTEND_HOST + instance.get_absolute_url(),
            )
            email = EmailMessage(title, msg, settings.DEFAULT_FROM_EMAIL, settings.ADMIN_EMAIL_LIST)
            email.send(fail_silently=True)
