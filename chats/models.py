from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    isArchive = models.BooleanField(default=0)

class Conversation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    lastModified = models.DateTimeField(auto_now_add=True, blank=True)
    messageId = models.ForeignKey(Message)

