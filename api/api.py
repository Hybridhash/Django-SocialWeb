from .serializers import *
from rest_framework import generics
from socialapp.models import Profile
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
import logging


class UserList(generics.ListAPIView):
    """
    GET request
    Fetches and returns a list of all users from the database
    """

    queryset = User.objects.all().distinct()
    serializer_class = UserSerializer


class CreateUser(generics.CreateAPIView):
    """
    Post request
    Inserts a new user into the database
    """

    serializer_class = UserSerializer


class ReadProfile(generics.RetrieveAPIView):
    """
    GET request
    Retrieves and returns the profile data of the specified user
    """

    lookup_field = "user__username"
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CreateProfile(generics.CreateAPIView):
    """
    Post request
    Create a new user and profile both to insert into database
    """

    serializer_class = ProfileSerializer


class UserPosts(generics.ListAPIView):
    """
    GET request
    Fetches all the posts created by a given user
    """

    queryset = Post.objects.all().distinct()
    serializer_class = PostSerializer

    """
    Get username from query parameter and filter by username
    """

    def filter_queryset(self, queryset):
        return queryset.filter(owner__username=self.kwargs.get("user__username"))
