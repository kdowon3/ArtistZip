# forms.py
from django import forms
from .models import Portfolio, Artwork

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description']

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image']

ArtworkFormSet = forms.inlineformset_factory(Portfolio, Artwork, form=ArtworkForm, extra=1, can_delete=True)
