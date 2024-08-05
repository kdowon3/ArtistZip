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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    image = models.ImageField(upload_to='portfolios/', null=True, blank=True)  # 완성본 이미지 파일
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Portfolio of {self.user.username}"

class ContactInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instagram = models.URLField(blank=True, verbose_name='Instagram')
    email = models.EmailField(blank=True, verbose_name='이메일')
    homepage = models.URLField(blank=True, verbose_name='홈페이지')

    def __str__(self):
        return f"{self.user.username}'s Contact Info"
