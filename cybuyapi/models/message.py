from django.db import models
from django.contrib.auth.models import User
from .conversation import Conversation


class Message(models.Model):

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Message")
        verbose_name_plural = ("Messages")


