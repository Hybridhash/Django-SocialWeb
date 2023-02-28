from django.urls import include, path
from . import views


urlpatterns = [
    path("chat/", views.ChatHome.as_view(), name="chat_home"),
    # path("chat/<str:room_name>/", views.ChatSpace.as_view(), name="chat_space"),
    #     path("chat/<str:slug>/", views.ChatHome.as_view(), name="chat_space"),
    #     path("chat/space_create", views.SpaceCreateView.as_view(), name="space_create"),
    #     path("chat/space_join", views.SpaceJoinView.as_view(), name="space_join"),
    path("chat/room/<str:slug>/", views.ChatRoom.as_view(), name="chat"),
    path("create/", views.RoomCreate.as_view(), name="room-create"),
    path("join/", views.paceJoin.as_view(), name="space_join"),
]
