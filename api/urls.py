from django.urls import path
from . import api


urlpatterns = [
    path("api/users/", api.UserList.as_view(), name="users_api"),
    path("api/create_user/", api.CreateUser.as_view(), name="create_user_api"),
    # To create both profile and user at same time
    path("api/create_profile/", api.CreateProfile.as_view(), name="create_profile_api"),
    path("api/read_profile/<str:user__username>/", api.ReadProfile.as_view(), name="read_profile_api"),
    path("api/user_posts/<str:user__username>/", api.UserPosts.as_view(), name="user_posts_api"),
]
