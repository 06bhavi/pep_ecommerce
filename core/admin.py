from django.contrib import admin
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'image_url')
    list_editable = ('active',)
