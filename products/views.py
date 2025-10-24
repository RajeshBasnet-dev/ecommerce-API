from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from api.permissions import IsSellerOrAdmin, IsAdmin

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            # Only admins can create categories
            permission_classes = [IsAdmin]
        else:
            # Anyone can list categories
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_201_CREATED)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only admins can update/delete categories
            permission_classes = [IsAdmin]
        else:
            # Anyone can view categories
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'success': True,
            'data': None,
            'error': None
        }, status=status.HTTP_204_NO_CONTENT)

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'seller', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'title']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            # Only sellers and admins can create products
            permission_classes = [IsSellerOrAdmin]
        else:
            # Anyone can list products
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
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
        # Check if user has a seller profile
        if not hasattr(request.user, 'seller_profile'):
            return Response({
                'success': False,
                'data': None,
                'error': 'User must have a seller profile to create products'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Set the seller to the current user's seller profile
        serializer.save(seller=request.user.seller_profile)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_201_CREATED)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only the seller of the product or admins can update/delete
            permission_classes = [IsSellerOrAdmin]
        else:
            # Anyone can view products
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Check if the user is the seller of this product or an admin
        if (hasattr(request.user, 'seller_profile') and 
            instance.seller == request.user.seller_profile) or \
           request.user.role == 'admin':
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'success': True,
                'data': serializer.data,
                'error': None
            })
        else:
            return Response({
                'success': False,
                'data': None,
                'error': 'You do not have permission to perform this action.'
            }, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user is the seller of this product or an admin
        if (hasattr(request.user, 'seller_profile') and 
            instance.seller == request.user.seller_profile) or \
           request.user.role == 'admin':
            self.perform_destroy(instance)
            return Response({
                'success': True,
                'data': None,
                'error': None
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                'success': False,
                'data': None,
                'error': 'You do not have permission to perform this action.'
            }, status=status.HTTP_403_FORBIDDEN)