from django.contrib import admin
<<<<<<< HEAD
from .models import Portfolio

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'created_at')
    search_fields = ('user__username', 'created_at')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    fields = ('user', 'image')  # 관리자가 편집할 수 있는 필드 설정

admin.site.register(Portfolio, PortfolioAdmin)
=======
from .models import Artwork

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_filter = ('user',)
>>>>>>> 4c3d81fefcf31cfa5335550a1ea079665b4dbd39
