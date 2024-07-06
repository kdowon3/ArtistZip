from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class ArtistSignupForm(UserCreationForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'required': True}))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'required': True}))

    class Meta:
        model = CustomUser
        fields = ['username', 'user_id', 'brand_name', 'password1', 'password2', 'email', 'contact_number']
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'user_id': forms.TextInput(attrs={'required': True}),
            'brand_name': forms.TextInput(attrs={'required': True}),
            'email': forms.EmailInput(attrs={'required': True}),
            'contact_number': forms.TextInput(attrs={'required': True}),
        }

class GeneralSignupForm(UserCreationForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'required': True}))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'required': True}))

    class Meta:
        model = CustomUser
        fields = ['username', 'user_id', 'company_name', 'position', 'password1', 'password2', 'email', 'contact_number']
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'user_id': forms.TextInput(attrs={'required': True}),
            'company_name': forms.TextInput(attrs={'required': False}),
            'position': forms.TextInput(attrs={'required': False}),
            'email': forms.EmailInput(attrs={'required': True}),
            'contact_number': forms.TextInput(attrs={'required': True}),
        }
