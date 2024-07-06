from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, verbose_name='이름')  # 이름
    user_id = models.CharField(max_length=150, unique=True, verbose_name='아이디')  # 아이디
    brand_name = models.CharField(max_length=150, verbose_name='브랜드명(작가명)')  # 브랜드명(작가명)
    company_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='회사명')  # 회사명(일반인)
    position = models.CharField(max_length=150, blank=True, null=True, verbose_name='직책')  # 직책(일반인)
    contact_number = models.CharField(max_length=15, verbose_name='연락처')  # 연락처
    is_artist = models.BooleanField(default=False, verbose_name='작가 여부')

    USERNAME_FIELD = 'user_id'  # 로그인을 user_id로
    REQUIRED_FIELDS = ['username', 'email', 'contact_number', 'brand_name']
    
    def __str__(self):
        return self.username
