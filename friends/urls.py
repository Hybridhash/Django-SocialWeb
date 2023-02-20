from django.urls import include, path
from . import views


urlpatterns = [
    path("friend/", views.Friends.as_view(), name="friend"),
]
