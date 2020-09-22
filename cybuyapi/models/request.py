from django.db import models
from django.contrib.auth.models import User

class Request(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=5000)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("Request")
        verbose_name_plural = ("Requests")



