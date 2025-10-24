from rest_framework import serializers
from .models import Wishlist
from products.serializers import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Wishlist
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
        
    def get_products_count(self, obj):
        return obj.products.count()