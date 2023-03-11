from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from socialapp.models import Profile, Post


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpass")
        self.profile = Profile.objects.create(
            user=self.user, country="US", birthdate=timezone.now().date(), image="images/test.jpg"
        )

    def test_profile_creation(self):
        """Test that a profile can be created"""
        self.assertIsInstance(self.profile, Profile)

    def test_profile_str(self):
        """Test that the profile string representation is correct"""
        expected = str(self.user.username)
        self.assertEqual(str(self.profile), expected)

    def test_profile_friends(self):
        """Test that friends can be added to a profile"""
        friend = Profile.objects.create(
            user=User.objects.create_user(username="frienduser", email="frienduser@example.com", password="friendpass"),
            country="CA",
            birthdate=timezone.now().date(),
            image="images/friend.jpg",
        )
        self.profile.friends.add(friend)
        self.assertIn(friend, self.profile.friends.all())

    def test_profile_friends_symmetry(self):
        """Test that the friendship relationship is not symmetrical"""
        friend = Profile.objects.create(
            user=User.objects.create_user(username="frienduser", email="frienduser@example.com", password="friendpass"),
            country="CA",
            birthdate=timezone.now().date(),
            image="images/friend.jpg",
        )
        self.profile.friends.add(friend)
        self.assertNotIn(self.profile, friend.friends.all())


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username="testuser", password="testpass")
        Post.objects.create(owner=test_user, text="This is a test post")

    def test_owner_label(self):
        """Test that a owner label can be created"""
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field("owner").verbose_name
        self.assertEqual(field_label, "owner")

    def test_text_max_length(self):
        """Test the length of maximum number of characters"""
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field("text").max_length
        self.assertEqual(max_length, 140)
