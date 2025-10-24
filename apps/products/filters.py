import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    seller = django_filters.CharFilter(field_name="seller__username", lookup_expr='icontains')
    in_stock = django_filters.BooleanFilter(field_name="stock", lookup_expr='gt')
    
    class Meta:
        model = Product
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'is_active': ['exact'],
        }

class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['icontains'],
        }