from rest_framework import serializers
from .models import Payout

class PayoutSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source='seller.store_name', read_only=True)
    
    class Meta:
        model = Payout
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'processed_at')