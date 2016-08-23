# Create your models here.
from django.db import models


class Gif(models.Model):
    name = models.CharField(max_length=256)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
