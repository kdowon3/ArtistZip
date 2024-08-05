from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, verbose_name='이름')
    user_id = models.CharField(max_length=150, unique=True, verbose_name='아이디')
    brand_name = models.CharField(max_length=150, verbose_name='브랜드명(작가명)')
    company_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='회사명')
    position = models.CharField(max_length=150, blank=True, null=True, verbose_name='직책')
    contact_number = models.CharField(max_length=15, verbose_name='연락처')
    is_artist = models.BooleanField(default=False, verbose_name='작가 여부')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    USERNAME_FIELD = 'user_id'  # 로그인을 user_id로
    REQUIRED_FIELDS = ['username', 'email', 'contact_number', 'brand_name']

    def __str__(self):
        return self.username

class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f"{self.subscriber.username} -> {self.subscribed_to.username}"
