from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from products.models import Product
from .serializers import WishlistSerializer

class WishlistView(generics.RetrieveAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        wishlist, created = Wishlist.objects.get_or_create(user=self.request.user)
        return wishlist
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })

class AddToWishlistView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        wishlist.products.add(product)
        
        serializer = self.get_serializer(wishlist)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_201_CREATED)

class RemoveFromWishlistView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'error': 'Product not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        wishlist.products.remove(product)
        
        return Response({
            'success': True,
            'data': None,
            'error': None
        }, status=status.HTTP_204_NO_CONTENT)