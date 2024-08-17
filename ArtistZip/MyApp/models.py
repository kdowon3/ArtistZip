from django.db import models
from django.conf import settings
from Auth.models import CustomUser

class Artwork(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artwork_image = models.ImageField(upload_to='artworks/', verbose_name='작품 이미지')
    artwork_title = models.CharField(max_length=150, verbose_name='작품명')
    artwork_description = models.TextField(verbose_name='작품 설명')

    def __str__(self):
        return self.artwork_title

class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolios')
    background_color = models.CharField(max_length=7, null=True, blank=True)
    author_name = models.CharField(max_length=100, default="Name")
    intro = models.CharField(max_length=200, null=True, blank=True, default="Appealing Description")
    career = models.TextField(max_length=200, null=True, blank=True, default="Career")
    photo1 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description1 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    photo2 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description2 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    photo3 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description3 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    photo4 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description4 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    photo5 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description5 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    photo6 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description6 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    photo7 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description7 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    photo8 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description8 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    photo9 = models.ImageField(upload_to='portfolio_images/', null=True, blank=True)
    description9 = models.CharField(max_length=100, null=True, blank=True, default="Project Name")
    instagram = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    template_number = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.author_name
    
    
    
class Special_Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='special_portfolios')
    photo = models.ImageField(upload_to='special_portfolio_images/', verbose_name='스페셜 포트폴리오 이미지')

    def __str__(self):
        return f"{self.user.username}'s Special Portfolio"