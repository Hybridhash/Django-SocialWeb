from django.db import models
from django.contrib.auth.models import User

# Model to track of the friend request
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="friend_requests_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="friend_requests_received", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )
    status = models.CharField(choices=STATUS_CHOICES, default="pending", max_length=20)
