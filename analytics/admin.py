from django.contrib import admin
from .models import SalesAnalytics, UserActivity

@admin.register(SalesAnalytics)
class SalesAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_sales', 'total_orders', 'total_products_sold', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('date',)
    readonly_fields = ('created_at',)
    ordering = ('-date',)
    list_per_page = 25

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'product', 'timestamp')
    list_filter = ('activity_type', 'timestamp', 'user')
    search_fields = ('user__username', 'user__email', 'activity_type', 'product__title')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    list_per_page = 25