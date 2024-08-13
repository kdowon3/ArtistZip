# MyApp/urls.py

from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='index'),
    path('artists/', views.artists, name='artists'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('myprofile/<int:user_id>/', views.myprofile, name='myprofile'),
    path('edit_artwork/<int:artwork_id>/', views.edit_artwork, name='edit_artwork'),
    path('delete_artwork/', views.delete_artwork, name='delete_artwork'),
    path('accounts/', include('allauth.urls')),  # django-allauth URLs 추가
    path('auth/', include('Auth.urls')),
    path('chat/', include('Chat.urls')),# auth 앱의 URLs 추가
    path('portfolio1/<int:user_id>/', views.portfolio1, name='portfolio1'),
    path('portfolio2/<int:user_id>/', views.portfolio2, name='portfolio2'),
    path('portfolio3/<int:user_id>/', views.portfolio3, name='portfolio3'),
    path('portfolio4/<int:user_id>/', views.portfolio4, name='portfolio4'),
    path('portfolio5/<int:user_id>/', views.portfolio5, name='portfolio5'),
    path('portfolio6/<int:user_id>/', views.portfolio6, name='portfolio6'),
    path('edit-contact-info/', views.edit_contact_info, name='edit_contact_info'),
    path('portfolio_upload/<int:user_id>/', views.portfolio_upload, name='portfolio_upload'),
    path('portfolio_list/<int:user_id>/', views.portfolio_list, name='portfolio_list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    