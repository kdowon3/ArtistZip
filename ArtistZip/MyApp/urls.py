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
    path('template/<int:user_id>/', views.template, name='template'),
    path('template/<int:user_id>/<int:artwork_id>/', views.template, name='template'),
    path('edit_artwork/<int:artwork_id>/', views.edit_artwork, name='edit_artwork'),
    path('delete_artwork/', views.delete_artwork, name='delete_artwork'),
    path('accounts/', include('allauth.urls')),  # django-allauth URLs 추가
    path('auth/', include('Auth.urls')),
    path('chat/', include('Chat.urls')),# auth 앱의 URLs 추가
    # Create portfolio views
    path('create_portfolio1/<int:user_id>/', views.create_portfolio1, name='create_portfolio1'),
    path('create_portfolio2/<int:user_id>/', views.create_portfolio2, name='create_portfolio2'),
    path('create_portfolio3/<int:user_id>/', views.create_portfolio3, name='create_portfolio3'),
    path('create_portfolio4/<int:user_id>/', views.create_portfolio4, name='create_portfolio4'),
    path('create_portfolio5/<int:user_id>/', views.create_portfolio5, name='create_portfolio5'),
    path('create_portfolio6/<int:user_id>/', views.create_portfolio6, name='create_portfolio6'),

    # Portfolio detail views
    path('portfolio_detail1/<int:user_id>/<int:portfolio_id>/', views.portfolio_detail1, name='portfolio_detail1'),
    path('portfolio_detail2/<int:user_id>/<int:portfolio_id>/', views.portfolio_detail2, name='portfolio_detail2'),
    path('portfolio_detail3/<int:user_id>/<int:portfolio_id>/', views.portfolio_detail3, name='portfolio_detail3'),
    path('portfolio_detail4/<int:user_id>/<int:portfolio_id>/', views.portfolio_detail4, name='portfolio_detail4'),
    path('portfolio_detail5/<int:user_id>/<int:portfolio_id>/', views.portfolio_detail5, name='portfolio_detail5'),
    path('portfolio_detail6/<int:user_id>/<int:portfolio_id>/', views.portfolio_detail6, name='portfolio_detail6'),
    path('view_my_portfolio/<int:user_id>/', views.view_my_portfolio, name='view_my_portfolio'),
    path('popup/',views.popup, name='popup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    