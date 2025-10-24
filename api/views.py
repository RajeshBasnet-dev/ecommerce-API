from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from apps.products.models import Product, Category
from apps.products.serializers import ProductSerializer, CategorySerializer

class GlobalSearchView(APIView):
    """
    Global search endpoint that searches across products and categories.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return Response({
                'success': False,
                'data': None,
                'error': 'Search query is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Search products
        product_results = Product.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
        
        # Search categories
        category_results = Category.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
        
        # Serialize results
        product_serializer = ProductSerializer(product_results, many=True)
        category_serializer = CategorySerializer(category_results, many=True)
        
        return Response({
            'success': True,
            'data': {
                'products': product_serializer.data,
                'categories': category_serializer.data,
                'total_products': product_results.count(),
                'total_categories': category_results.count()
            },
            'error': None
        })