# forms.py
from django import forms
from .models import Artwork

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['artwork_image', 'artwork_title', 'artwork_description', 'author_name', 'author_info', 'art_description']
