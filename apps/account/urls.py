from django.urls import path
from apps.account import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("create/", views.UserCreate.as_view(), name="create"),
]
