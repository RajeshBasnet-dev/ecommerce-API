from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'shipped_at', 'delivered_at')
    list_filter = ('status', 'created_at', 'shipped_at', 'delivered_at', 'user')
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('created_at', 'updated_at', 'shipped_at', 'delivered_at', 'total_price')
    ordering = ('-created_at',)
    list_per_page = 25
    inlines = [OrderItemInline]
    
    actions = ['mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']

    @admin.action(description="Mark selected orders as shipped")
    def mark_as_shipped(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='shipped', shipped_at=timezone.now())

    @admin.action(description="Mark selected orders as delivered")
    def mark_as_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='delivered', delivered_at=timezone.now())

    @admin.action(description="Mark selected orders as cancelled")
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'total_price')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('order__id', 'product__title')
    readonly_fields = ('order', 'product', 'quantity', 'price', 'total_price')
    ordering = ('-order__created_at',)

    @admin.display(description='Total Price')
    def total_price(self, obj):
        return obj.quantity * obj.price