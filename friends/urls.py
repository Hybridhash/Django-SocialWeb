from django.urls import include, path
from . import views

# Friend app URL's
urlpatterns = [
    path("friends/", views.FriendHome.as_view(), name="friends"),
    path("friend_add/<int:pk>/", views.FriendCreate.as_view(), name="friend_add"),
    path("friend_accept/<int:pk>/", views.FriendAccept.as_view(), name="friend_accept"),
    path("friend_delete/<int:pk>/", views.FriendDelete.as_view(), name="friend_delete"),
]
