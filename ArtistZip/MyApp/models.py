from django.db import models
from django.conf import settings

class Artwork(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork_image = models.ImageField(upload_to='artworks/', verbose_name='작품 이미지')
    author_name = models.CharField(max_length=100, verbose_name='작가명', blank=True, null=True)
    author_info = models.TextField(verbose_name='작가 설명', blank=True, null=True)
    art_description = models.TextField(verbose_name='작품 상세 설명', blank=True, null=True)
    art_title = models.CharField(max_length=150, verbose_name='작품 제목', blank=True, null=True)

    def __str__(self):
        return self.art_title
