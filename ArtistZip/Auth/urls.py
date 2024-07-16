# auth/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/artist/', views.artist_signup, name='artist_signup'),
    path('signup/general/', views.general_signup, name='general_signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('link-account/', views.link_account, name='link_account'),
    path('cancel-link/', views.cancel_link, name='cancel_link'),
]

