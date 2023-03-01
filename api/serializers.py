from django.contrib.auth.models import User
from rest_framework import serializers
from socialapp.models import Profile, Post
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    friends = serializers.StringRelatedField(many=True, source="followed_by")

    class Meta:
        model = Profile
        fields = ("user", "birthdate", "image", "friends")

    def get_friends(self, obj):
        return [friend.user.username for friend in obj.friends.all()]

    def create(self, validated_data):

        # create user
        user = User.objects.create(
            username=validated_data["user"]["username"],
            first_name=validated_data["user"]["first_name"],
            last_name=validated_data["user"]["last_name"],
            email=validated_data["user"]["email"],
        )

        # create profile
        profile = Profile.objects.create(
            user=user,
            birthdate=validated_data["birthdate"],
            image=validated_data["image"],
        )

        return profile


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("text", "image")
