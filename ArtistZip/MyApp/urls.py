# MyApp/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('az/', views.az, name='az'),
    path('artists/', views.artists, name='artists'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('myprofile/<int:user_id>/', views.myprofile, name='myprofile'),
    path('template/<int:user_id>/', views.template, name='template'),
    path('edit_artwork/<int:artwork_id>/', views.edit_artwork, name='edit_artwork'),
    path('delete_artwork/', views.delete_artwork, name='delete_artwork'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)