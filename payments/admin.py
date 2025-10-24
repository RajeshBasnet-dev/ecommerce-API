from django.contrib import admin
from .models import Payout

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('seller', 'amount', 'status', 'transaction_id', 'created_at', 'processed_at')
    list_filter = ('status', 'created_at', 'processed_at', 'seller')
    search_fields = ('seller__store_name', 'transaction_id')
    readonly_fields = ('created_at', 'processed_at')
    ordering = ('-created_at',)
    list_per_page = 25
    
    actions = ['mark_as_completed', 'mark_as_failed']

    @admin.action(description="Mark selected payouts as completed")
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description="Mark selected payouts as failed")
    def mark_as_failed(self, request, queryset):
        queryset.update(status='failed')