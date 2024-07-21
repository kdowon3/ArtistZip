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
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('myprofile/<int:user_id>/', views.myprofile, name='myprofile'),
    path('template/<int:user_id>/', views.template, name='template'),
    path('template/<int:user_id>/<int:artwork_id>/', views.template, name='template'),
    path('edit_artwork/<int:artwork_id>/', views.edit_artwork, name='edit_artwork'),
    path('delete_artwork/', views.delete_artwork, name='delete_artwork'),
    path('portfolio1/', views.portfolio1, name='portfolio1'),
    path('portfolio2/', views.portfolio2, name='portfolio2'),
    path('portfolio3/', views.portfolio3, name='portfolio3'),
    path('portfolio4/', views.portfolio4, name='portfolio4'),
    path('portfolio5/', views.portfolio5, name='portfolio5'),
    path('portfolio6/', views.portfolio6, name='portfolio6'),
    path('edit-contact-info/', views.edit_contact_info, name='edit_contact_info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)