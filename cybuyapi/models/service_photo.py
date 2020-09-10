from django.db import models
from .service import Service

class ServicePhoto(models.Model):

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=500)


    class Meta:
        verbose_name = ("ServicePhoto")
        verbose_name_plural = ("ServicePhotos")

    def __str__(self):
        return self.name


