from django.db import models
from django.conf import settings

class Artwork(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork_image = models.ImageField(upload_to='artworks/', verbose_name='작품 이미지')
    artwork_title = models.CharField(max_length=150, verbose_name='작품명')
    artwork_description = models.TextField(verbose_name='작품 설명')
    
    image1 = models.ImageField(upload_to='artworks/', verbose_name='이미지 1', blank=True, null=True)
    image2 = models.ImageField(upload_to='artworks/', verbose_name='이미지 2', blank=True, null=True)
    image3 = models.ImageField(upload_to='artworks/', verbose_name='이미지 3', blank=True, null=True)
    image4 = models.ImageField(upload_to='artworks/', verbose_name='이미지 4', blank=True, null=True)
    image5 = models.ImageField(upload_to='artworks/', verbose_name='이미지 5', blank=True, null=True)
    image6 = models.ImageField(upload_to='artworks/', verbose_name='이미지 6', blank=True, null=True)

    author_name = models.CharField(max_length=100, verbose_name='작가명', blank=True, null=True)
    author_info = models.TextField(verbose_name='작가 설명', blank=True, null=True)
    art_description = models.TextField(verbose_name='작품 상세 설명', blank=True, null=True)
    art_title = models.CharField(max_length=150, verbose_name='작품 제목', blank=True, null=True)

    def __str__(self):
        return self.artwork_title
