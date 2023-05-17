from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Authentication
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

# Models
from django.contrib.auth.models import User

# Serializers
from apps.account.serializers import UserLoginSerializer


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
