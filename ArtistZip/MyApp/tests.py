# myapp/models.py

from django.db import models
from django.conf import settings

class Artwork(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    artwork_image = models.ImageField(upload_to='artworks/')
    artwork_title = models.CharField(max_length=200)
    artwork_description = models.TextField()

    def __str__(self):
        return self.artwork_title