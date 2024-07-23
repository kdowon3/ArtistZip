# myapp/models.py

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = 1, related_name='portfolios')
    author_name = models.CharField(max_length=255, verbose_name='작가명')
    art_title = models.CharField(max_length=255, verbose_name='작품 제목')
    art_description = models.TextField(verbose_name='작품 설명')

    def __str__(self):
        return self.art_title

class ContactInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instagram = models.URLField(blank=True, verbose_name='Instagram')
    email = models.EmailField(blank=True, verbose_name='이메일')
    homepage = models.URLField(blank=True, verbose_name='홈페이지')

    def __str__(self):
        return f"{self.user.username}'s Contact Info"
