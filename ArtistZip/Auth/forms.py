from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
import re

class ArtistSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'required': True, 'class': 'artist-signup-input'}))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'required': True, 'class': 'artist-signup-input'}))
    contact_number = forms.CharField(label='연락처', widget=forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'user_id', 'brand_name', 'email', 'contact_number']
        widgets = {
            'username': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'user_id': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'brand_name': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'email': forms.EmailInput(attrs={'required': True, 'class': 'artist-signup-input'}),
            'contact_number': forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}),
        }

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        
        # Remove any non-digit characters (except hyphens)
        cleaned_number = re.sub(r'[^\d-]', '', contact_number)

        # Check if the cleaned number is in a valid format
        if not re.match(r'^\d{2,3}-\d{3,4}-\d{4}$', cleaned_number):
            raise forms.ValidationError(_('올바른 연락처를 입력하세요.'))

        return cleaned_number
        
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError(_("비밀번호는 최소 8자 이상이어야 합니다."))
        if not re.match(r'^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z\d]{8,}$', password1):
            raise forms.ValidationError(_("비밀번호는 영문자와 숫자의 조합으로 최소 8자 이상이어야 합니다."))
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("비밀번호가 일치하지 않습니다."))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class GeneralSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'required': True, 'class': 'artist-signup-input'}))
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'required': True, 'class': 'artist-signup-input'}))
    contact_number = forms.CharField(label='연락처', widget=forms.TextInput(attrs={'required': True, 'class': 'artist-signup-input'}))
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

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        
        # Remove any non-digit characters (except hyphens)
        cleaned_number = re.sub(r'[^\d-]', '', contact_number)

        # Check if the cleaned number is in a valid format
        if not re.match(r'^\d{2,3}-\d{3,4}-\d{4}$', cleaned_number):
            raise forms.ValidationError(_('올바른 연락처를 입력하세요.'))

        return cleaned_number
        
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError(_("비밀번호는 최소 8자 이상이어야 합니다."))
        if not re.match(r'^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z\d]{8,}$', password1):
            raise forms.ValidationError(_("비밀번호는 영문자와 숫자의 조합으로 최소 8자 이상이어야 합니다."))
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("비밀번호가 일치하지 않습니다."))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
