from django.contrib import admin
from django.contrib.auth import views as authentication_views
from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("register_google/", views.GoogleOAuthView.as_view(), name="register_google"),
    path("login/", views.Login, name="login"),
    path(
        "logout/",
        authentication_views.LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
]
