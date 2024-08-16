from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html
from .models import Portfolio

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'template_link', 'email', 'instagram', 'website', 'background_color')

    def template_link(self, obj):
        if obj.template_number:
            view_name = f'portfolio_detail{obj.template_number}'
            try:
                url = reverse(view_name, args=[obj.user_id, obj.id])
                return format_html('<a href="{}">View Portfolio</a>', url)
            except NoReverseMatch:
                return "Invalid URL"
        return "No template assigned"

    template_link.short_description = 'Portfolio Link'

    def background_color_display(self, obj):
        if obj.background_color:
            return format_html('<div style="background-color:{}; width:100px; height:20px;"></div>', obj.background_color)
        return "No color set"

    background_color_display.short_description = 'Background Color'

admin.site.register(Portfolio, PortfolioAdmin)
