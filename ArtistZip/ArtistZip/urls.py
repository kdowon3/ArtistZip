from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MyApp.urls')),
    path('accounts/', include('allauth.urls')),  # django-allauth URLs 추가
    path('auth/', include('Auth.urls')),         # auth 앱의 URLs 추가
]