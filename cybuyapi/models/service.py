from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=5000)

    class Meta:
        verbose_name = ("Service")
        verbose_name_plural = ("Services")


