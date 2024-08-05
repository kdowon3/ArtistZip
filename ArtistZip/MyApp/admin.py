from django.contrib import admin
from .models import Portfolio

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'created_at')
    search_fields = ('user__username', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    fields = ('user', 'image')  # 관리자가 편집할 수 있는 필드 설정

admin.site.register(Portfolio, PortfolioAdmin)
