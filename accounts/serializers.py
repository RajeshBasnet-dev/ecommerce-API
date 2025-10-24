from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from sellers.models import SellerProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'first_name', 'last_name', 'phone_number', 'date_of_birth')
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class SellerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = SellerProfile
        fields = '__all__'
        read_only_fields = ('id', 'user', 'earnings')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        return token

class UserProfileSerializer(serializers.ModelSerializer):
    seller_profile = SellerProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'seller_profile')
        read_only_fields = ('id', 'role')