# forms.py
from django import forms
from .models import Artwork, Portfolio, Special_Portfolio

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['artwork_image', 'artwork_title', 'artwork_description']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        exclude = ['user']  # user 필드를 제외
        
        
        
class SpecialPortfolioForm(forms.ModelForm):
    class Meta:
        model = Special_Portfolio
        fields = ['photo']