# myapp/forms.py

from django import forms
from .models import Artwork

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['artist_name', 'artwork_image', 'artwork_title', 'artwork_description']
