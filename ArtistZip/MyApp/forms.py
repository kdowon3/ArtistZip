# forms.py
from django import forms
from .models import Artwork

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
<<<<<<< HEAD
        fields = ['artwork_image', 'artwork_title', 'artwork_description']

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['instagram', 'email', 'homepage']

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['image']
=======
        fields = ['artwork_image', 'author_name', 'author_info', 'art_description', 'art_title']
>>>>>>> 4c3d81fefcf31cfa5335550a1ea079665b4dbd39
