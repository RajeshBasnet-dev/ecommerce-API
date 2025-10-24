from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('added_at', 'total_price')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    list_per_page = 25
    inlines = [CartItemInline]

    @admin.display(description='Number of Items')
    def item_count(self, obj):
        return obj.items.count()

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'added_at', 'total_price')
    list_filter = ('added_at', 'cart__user')
    search_fields = ('cart__user__username', 'product__title')
    readonly_fields = ('added_at', 'total_price')
    ordering = ('-added_at',)