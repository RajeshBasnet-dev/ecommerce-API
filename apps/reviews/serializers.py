from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')