# MyApp/urls.py

from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('az/', views.az, name='az'),
    path('artists/', views.artists, name='artists'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('auth/', include('Auth.urls')),
    
]