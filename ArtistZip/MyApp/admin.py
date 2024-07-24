from django.contrib import admin
from .models import Artwork, Portfolio

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'portfolio')
    list_filter = ('user', 'portfolio')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    list_filter = ('user',)
