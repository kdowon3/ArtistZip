# MyApp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('az/', views.az, name='az'),
    path('artists/', views.artists, name='artists'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('artist_signup/', views.artist_signup, name='artist_signup'),
    path('normal_signup/', views.normal_signup, name='normal_signup'),
    path('profile/', views.profile, name='profile'),
]
