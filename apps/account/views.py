from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView


def redirect_admin(request):
    """Redirects to django admin page"""
    return redirect(reverse_lazy("admin:index"))


class Ping(APIView):
    """Check service ping"""
    def get(self, request):
        return Response({"response": "pong!"})
