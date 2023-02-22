from django.urls import include, path
from . import views


urlpatterns = [
    path("friends/", views.FriendHome.as_view(), name="friends"),
    path("friend_add/<int:pk>/", views.FriendCreate.as_view(), name="friend_add"),
]
