import json
from rest_framework import permissions, status, serializers
from django.contrib.auth import get_user_model  # If used custom user model

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        return user

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name"
        )


class StringListField(serializers.ListField):
    day = serializers.CharField(allow_blank=False, min_length=2, max_length=400)


class ScheduleJobSerializer(serializers.Serializer):
    target_name = serializers.CharField(allow_blank=False, min_length=2, max_length=400)
    days_of_week = StringListField()
    schedule_time = serializers.DateTimeField()

    class Meta:
        fields = ("target_name", "schedule_time", "days_of_week")


class HitJobSerializer(serializers.Serializer):
    target_name = serializers.CharField(allow_blank=False, min_length=2, max_length=400)

    class Meta:
        fields = "target_name"
