from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ChatSpace(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    users = models.ManyToManyField(User)


class ChatMessage(models.Model):
    space = models.ForeignKey(ChatSpace, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
