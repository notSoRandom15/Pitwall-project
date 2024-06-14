from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Channel(models.Model):
    sender_user = models.ForeignKey(User, related_name='sent_channels', on_delete=models.CASCADE)
    recipient_user = models.ForeignKey(User, related_name='received_channels', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, null=True)
    accepted = models.BooleanField(default=False)
    initial_sender_secret = models.TextField()
    initial_recipient_secret = models.TextField()
