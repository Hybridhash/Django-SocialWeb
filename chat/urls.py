from django.urls import include, path
from . import views


urlpatterns = [
    path("chat/", views.ChatHome.as_view(), name="chat_home"),
    path("chat/room/<str:slug>/", views.ChatRoom.as_view(), name="chat"),
    path("create/", views.SpaceCreate.as_view(), name="space_create"),
    path("join/", views.SpaceJoin.as_view(), name="space_join"),
]
