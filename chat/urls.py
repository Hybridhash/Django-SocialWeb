from django.urls import include, path
from . import views


urlpatterns = [
    path("chat/", views.chat_home, name="chat"),
    path("chat/<str:space_name>/", views.chat_space, name="chat_space"),
]
