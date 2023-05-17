from django.urls import path
from apps.account import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
]
