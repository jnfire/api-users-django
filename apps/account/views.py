from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Models
from django.contrib.auth.models import User
from apps.account.models import Profile

# Serializers
from apps.account.serializers import UserLoginSerializer, ProfileGetSerializer, ProfileUpdateSerializer

# Files
from django.core.files.base import ContentFile
import base64
import time



def redirect_admin(request):
    """Redirects to django admin page"""
    return redirect(reverse_lazy("admin:index"))


class Ping(APIView):
    """Check service ping"""
    def get(self, request):
        return Response({"response": "pong!"})


class Login(ObtainAuthToken):
    """Login user"""
    def post(self, request, *args, **kwargs):
        # Default data
        # Get data from request
        serializer = UserLoginSerializer(data=request.data)
        # Validate data
        if serializer.is_valid():
            # Get serializer data
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            # Get user
            user = User.objects.filter(email=email).first()
            if user:
                # Check if user is active
                if user.is_active:
                    # Check password
                    if user.check_password(password):
                        # Search old tokens
                        old_tokens = Token.objects.filter(user=user)
                        if old_tokens:
                            # Delete old tokens
                            old_tokens.delete()
                        # Create token
                        token, created = Token.objects.get_or_create(user=user)
                        return Response(
                            data={"token": token.key},
                            status=status.HTTP_200_OK,
                        )
                    return Response(
                        data={"response": "Password not valid"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                return Response(
                    data={"response": "Is not active"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return Response(
                data={"response": "Email not valid or does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class Logout(APIView):
    """Logout user"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get user
        user = request.user
        # Search old tokens
        old_tokens = Token.objects.filter(user=user)
        if old_tokens:
            # Delete old tokens
            old_tokens.delete()
        return Response(
            data={"response": "Logout success"},
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    """Get user profile"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Get user profile"""
        # Get user profile
        profile = Profile.objects.filter(user=request.user).first()
        # Serialize data
        serializer = ProfileGetSerializer(profile)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():

            def get_value_without_none(old_value, new_value):
                """Filter that returns the old_value if the new_value is None"""
                if new_value and old_value != new_value:
                    return new_value
                return old_value

            # Update user
            user.email = get_value_without_none(
                old_value=user.email,
                new_value=serializer.validated_data.get("email")
            )
            user.first_name = get_value_without_none(
                old_value=user.first_name,
                new_value=serializer.validated_data.get("first_name")
            )
            user.last_name = get_value_without_none(
                old_value=user.last_name,
                new_value=serializer.validated_data.get("last_name")
            )
            user.save()

            # Update profile
            # Get avatar
            avatar = serializer.validated_data.get("avatar")
            # Update avatar
            if (
                avatar
                and avatar.get("name")
                and avatar.get("base64")
            ):
                try:
                    # Get profile
                    profile = Profile.objects.filter(user=user).first()
                    # Get file
                    file = avatar.get("base64")
                    # Check file is base64
                    if base64.b64encode(base64.b64decode(file)).decode("utf-8") == file:
                        # Decode file
                        new_file = ContentFile(
                            base64.b64decode(file), avatar.get("name")
                        )
                        # Check file size is less than 5mb
                        if new_file.size <= 5728640:
                            # Upload file
                            profile.avatar.save(
                                f"{int(time.time() * 1000)}_{new_file.name}", new_file
                            )
                        else:
                            return Response(
                                dict(
                                    response="El archivo es demasiado grande, debe ser menor o igual a 5mb"
                                ),
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                except Exception:
                    return Response(
                        dict(response="El archivo no es base64"),
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
