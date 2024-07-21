from django.db import models
from django.conf import settings

class Artwork(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork_image = models.ImageField(upload_to='artworks/', verbose_name='작품 이미지')
    artwork_title = models.CharField(max_length=150, verbose_name='작품명')
    artwork_description = models.TextField(verbose_name='작품 설명')

    def __str__(self):
        return self.artwork_title

class Portfolio(models.Model):
    author_name = models.CharField(max_length=255)
    art_title = models.CharField(max_length=255)
    art_description = models.TextField()
    
    
class ContactInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instagram = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    homepage = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Contact Info"