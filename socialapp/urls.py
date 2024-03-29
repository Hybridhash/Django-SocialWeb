from django.urls import include, path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path("home/", views.Home.as_view(), name="home"),
    path("login/", views.user_login, name="login"),
    path("profile/<str:username>/", views.user_profile, name="profile"),
    path("profile_update/", views.UserProfileEdit.as_view(), name="profile_update"),
    path("profile_create/", views.UserProfileCreate.as_view(), name="profile_create"),
    path("post_create/", views.PostCreate.as_view(), name="post_create"),
    path("post/<int:pk>/edit/", views.PostUpdate.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDelete.as_view(), name="post_delete"),
]
