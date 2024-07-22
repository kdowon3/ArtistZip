# myapp/forms.py

from django import forms
from .models import Artwork, ContactInfo, Portfolio

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['artwork_image', 'artwork_title', 'artwork_description']

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['instagram', 'email', 'homepage']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['author_name', 'art_title', 'art_description']
