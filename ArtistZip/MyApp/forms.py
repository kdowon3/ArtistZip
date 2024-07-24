# forms.py
from django import forms
from .models import Artwork

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['artwork_image', 'author_name', 'author_info', 'art_description', 'art_title']
