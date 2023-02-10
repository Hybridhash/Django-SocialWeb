from django.urls import include, path
from . import views

# Importing the API's
# from . import api

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.user_signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("home/", views.homepage, name="home"),
    path("simple_login/", views.user_login, name="login"),
]
