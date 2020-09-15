from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):

    user = models.ForeignKey(User, related_name="conversation_user", on_delete=models.CASCADE)
    other_user = models.ForeignKey(User, related_name="conversation_other_user", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Conversation")
        verbose_name_plural = ("Conversations")

