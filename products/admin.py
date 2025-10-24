from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    list_per_page = 25

    @admin.display(description='Number of Products')
    def product_count(self, obj):
        return obj.products.count()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at', 'seller')
    search_fields = ('title', 'description', 'seller__store_name', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25
    list_editable = ('is_active', 'stock')
    
    actions = ['make_active', 'make_inactive', 'restock_products']

    @admin.action(description="Mark selected products as active")
    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected products as inactive")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Restock selected products (+100 units)")
    def restock_products(self, request, queryset):
        for product in queryset:
            product.stock += 100
            product.save()