from django.contrib import admin
from .models import SellerProfile

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'is_verified', 'earnings', 'created_at', 'updated_at')
    list_filter = ('is_verified', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'store_name')
    readonly_fields = ('earnings', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25
    
    actions = ['verify_sellers', 'unverify_sellers']

    @admin.action(description="Verify selected sellers")
    def verify_sellers(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description="Unverify selected sellers")
    def unverify_sellers(self, request, queryset):
        queryset.update(is_verified=False)