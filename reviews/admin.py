from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at', 'updated_at', 'product__category')
    search_fields = ('user__username', 'user__email', 'product__title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25