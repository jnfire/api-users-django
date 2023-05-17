from django.shortcuts import redirect
from django.urls import reverse_lazy


def redirect_admin(request):
    """Redirects to django admin page"""
    return redirect(reverse_lazy("admin:index"))
