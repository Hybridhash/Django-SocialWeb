from django.urls import include, path
from . import views


urlpatterns = [
    path("friends/", views.Friends.as_view(), name="friends"),
    path("friend_add/<int:pk>/", views.FriendCreate.as_view(), name="friend_add"),
]
