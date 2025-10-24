from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SellerProfile
from products.models import Product
from orders.models import Order
from .serializers import SellerProfileSerializer
from products.serializers import ProductSerializer
from orders.serializers import OrderSerializer

class SellerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Return the seller profile for the current user
        try:
            return SellerProfile.objects.get(user=self.request.user)
        except SellerProfile.DoesNotExist:
            return None
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({
                'success': False,
                'data': None,
                'error': 'Seller profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return Response({
                'success': False,
                'data': None,
                'error': 'Seller profile not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })

class SellerProductListView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return products for the current seller
        if self.request.user.role == 'seller':
            try:
                seller_profile = SellerProfile.objects.get(user=self.request.user)
                return Product.objects.filter(seller=seller_profile)
            except SellerProfile.DoesNotExist:
                return Product.objects.none()
        return Product.objects.none()
    
    def perform_create(self, serializer):
        # Associate the product with the current seller
        try:
            seller_profile = SellerProfile.objects.get(user=self.request.user)
            serializer.save(seller=seller_profile)
        except SellerProfile.DoesNotExist:
            pass
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data,
                'error': None
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })
    
    def create(self, request, *args, **kwargs):
        if request.user.role != 'seller':
            return Response({
                'success': False,
                'data': None,
                'error': 'Only sellers can create products'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if user has a seller profile
        try:
            seller_profile = SellerProfile.objects.get(user=request.user)
        except SellerProfile.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'error': 'Seller profile not found'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_201_CREATED)

class SellerOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return orders for products sold by the current seller
        if self.request.user.role == 'seller':
            try:
                seller_profile = SellerProfile.objects.get(user=self.request.user)
                # Get orders that contain products from this seller
                return Order.objects.filter(items__product__seller=seller_profile).distinct()
            except SellerProfile.DoesNotExist:
                return Order.objects.none()
        return Order.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'success': True,
                'data': serializer.data,
                'error': None
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })