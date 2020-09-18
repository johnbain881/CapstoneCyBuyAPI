from django.db import models
from .request import Request

class RequestPhoto(models.Model):

    request = models.ForeignKey(Request, related_name="photos", on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=500)


    class Meta:
        verbose_name = ("RequestPhoto")
        verbose_name_plural = ("RequestPhotos")



