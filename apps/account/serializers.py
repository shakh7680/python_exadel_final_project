from rest_framework import serializers
from . import models


class UserlocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ("id", "image", "first_name", "last_name", "phone_number")
