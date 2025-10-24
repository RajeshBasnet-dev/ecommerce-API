from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role', 'first_name', 'last_name', 'phone_number', 'date_of_birth')
        read_only_fields = ('id',)
    
    def validate_password(self, value):
        """
        Validate password strength
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class SellerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = 'sellers.SellerProfile'  # Use string reference to avoid circular import
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
    # Use a SerializerMethodField to safely handle seller_profile
    seller_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'seller_profile')
        read_only_fields = ('id', 'role')
    
    def get_seller_profile(self, obj):
        # Safely get seller profile if it exists
        try:
            if hasattr(obj, 'seller_profile'):
                serializer = SellerProfileSerializer(obj.seller_profile)
                return serializer.data
            return None
        except:
            return None