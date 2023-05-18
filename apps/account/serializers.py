from rest_framework import serializers
from django.contrib.auth.models import User
from apps.account.models import Profile


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password"]


class ProfileGetSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField("get_email")
    first_name = serializers.SerializerMethodField("get_first_name")
    last_name = serializers.SerializerMethodField("get_last_name")
    avatar_url = serializers.SerializerMethodField("get_avatar")

    def get_email(self, profile):
        return profile.user.email

    def get_first_name(self, profile):
        return profile.user.first_name

    def get_last_name(self, profile):
        return profile.user.last_name

    def get_avatar(self, profile):
        return profile.avatar_url

    class Meta:
        model = Profile
        fields = ["name", "email", "first_name", "last_name", "avatar_url"]


class AvatarFileSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    base64 = serializers.CharField(required=False, allow_blank=True)


class ProfileUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    avatar = AvatarFileSerializer(required=False)
