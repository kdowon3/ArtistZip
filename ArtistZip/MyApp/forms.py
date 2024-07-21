# myapp/forms.py

from django import forms
from .models import Artwork, ContactInfo

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['artwork_image', 'artwork_title', 'artwork_description']


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['instagram', 'email', 'homepage']