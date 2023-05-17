from rest_framework import serializers
from django.contrib.auth.models import User

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password"]
