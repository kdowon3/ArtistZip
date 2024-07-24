from django.db import models
from django.conf import settings

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=255, verbose_name='포트폴리오 제목', blank=True, null=True)
    description = models.TextField(verbose_name='포트폴리오 설명', blank=True, null=True)

    def __str__(self):
        return self.title if self.title else 'Untitled Portfolio'

class Artwork(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, related_name='artworks', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='작품 제목', blank=True, null=True)
    description = models.TextField(verbose_name='작품 설명', blank=True, null=True)
    image = models.ImageField(upload_to='artworks/', verbose_name='작품 이미지', blank=True, null=True)
    
    def __str__(self):
        return self.title if self.title else 'Untitled Artwork'
