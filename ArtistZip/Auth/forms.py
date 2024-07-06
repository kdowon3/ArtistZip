from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ArtistSignupForm(UserCreationForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'required': True, 'class': 'artist-signup-input'}))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'required': True, 'class': 'artist-signup-input'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'user_id', 'brand_name', 'password1', 'password2', 'email', 'contact_number']
        widgets = {
            'username': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'user_id': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'brand_name': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'email': forms.EmailInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'contact_number': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
        }

class GeneralSignupForm(UserCreationForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'required': True, 'class': 'artist-signup-input'}))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'required': True, 'class': 'artist-signup-input'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'user_id', 'company_name', 'position', 'password1', 'password2', 'email', 'contact_number']
        widgets = {
            'username': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'user_id': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'company_name': forms.TextInput(attrs={'required': False, 'class': 'artist-signup-input'}),
            'position': forms.TextInput(attrs={'required': False, 'class': 'artist-signup-input'}),
            'email': forms.EmailInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'contact_number': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
        }
