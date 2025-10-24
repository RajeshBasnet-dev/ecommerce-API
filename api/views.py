from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action


class APIIndexViewSet(viewsets.ViewSet):
    """ViewSet for the API index endpoint"""
    permission_classes = [AllowAny]
    
    def list(self, request):
        """Return the API index with all available endpoints"""
        endpoints = {
            'Authentication': [
                {'name': 'Obtain JWT Token', 'url': '/api/token/', 'method': 'POST', 'description': 'Get access and refresh tokens'},
                {'name': 'Refresh JWT Token', 'url': '/api/token/refresh/', 'method': 'POST', 'description': 'Refresh access token'},
                {'name': 'User Registration', 'url': '/api/auth/register/', 'method': 'POST', 'description': 'Register a new user'},
                {'name': 'User Login', 'url': '/api/auth/login/', 'method': 'POST', 'description': 'Login and obtain tokens'},
                {'name': 'User Logout', 'url': '/api/auth/logout/', 'method': 'POST', 'description': 'Logout and blacklist token'},
                {'name': 'User Profile', 'url': '/api/auth/profile/', 'method': 'GET/PUT', 'description': 'View or update user profile'},
            ],
            'Products': [
                {'name': 'List/Create Products', 'url': '/api/products/', 'method': 'GET/POST', 'description': 'List all products or create a new one'},
                {'name': 'Product Detail', 'url': '/api/products/{id}/', 'method': 'GET/PUT/DELETE', 'description': 'View, update, or delete a specific product'},
                {'name': 'List/Create Categories', 'url': '/api/products/categories/', 'method': 'GET/POST', 'description': 'List all categories or create a new one'},
                {'name': 'Category Detail', 'url': '/api/products/categories/{id}/', 'method': 'GET/PUT/DELETE', 'description': 'View, update, or delete a specific category'},
            ],
            'Orders': [
                {'name': 'List/Create Orders', 'url': '/api/orders/', 'method': 'GET/POST', 'description': 'List user orders or create a new one'},
                {'name': 'Order Detail', 'url': '/api/orders/{id}/', 'method': 'GET/PUT', 'description': 'View or update a specific order'},
            ],
            'Cart': [
                {'name': 'View Cart', 'url': '/api/cart/', 'method': 'GET', 'description': 'View current user cart'},
                {'name': 'Add to Cart', 'url': '/api/cart/add/', 'method': 'POST', 'description': 'Add item to cart'},
                {'name': 'Update Cart Item', 'url': '/api/cart/update/{id}/', 'method': 'PUT', 'description': 'Update cart item quantity'},
                {'name': 'Remove from Cart', 'url': '/api/cart/remove/{id}/', 'method': 'DELETE', 'description': 'Remove item from cart'},
            ],
            'Reviews': [
                {'name': 'List/Create Product Reviews', 'url': '/api/reviews/products/{product_id}/', 'method': 'GET/POST', 'description': 'List reviews for a product or create a new review'},
                {'name': 'Review Detail', 'url': '/api/reviews/{id}/', 'method': 'GET/PUT/DELETE', 'description': 'View, update, or delete a specific review'},
            ],
            'Messaging': [
                {'name': 'List/Create Order Messages', 'url': '/api/messages/orders/{order_id}/', 'method': 'GET/POST', 'description': 'List messages for an order or create a new message'},
                {'name': 'Message Detail', 'url': '/api/messages/{id}/', 'method': 'GET/PUT/DELETE', 'description': 'View, update, or delete a specific message'},
            ],
            'Wishlist': [
                {'name': 'View Wishlist', 'url': '/api/wishlist/', 'method': 'GET', 'description': 'View user wishlist'},
                {'name': 'Add to Wishlist', 'url': '/api/wishlist/add/', 'method': 'POST', 'description': 'Add item to wishlist'},
                {'name': 'Remove from Wishlist', 'url': '/api/wishlist/remove/', 'method': 'POST', 'description': 'Remove item from wishlist'},
            ],
            'Seller': [
                {'name': 'Seller Profile', 'url': '/api/seller/profile/', 'method': 'GET/PUT', 'description': 'View or update seller profile'},
                {'name': 'Seller Products', 'url': '/api/seller/products/', 'method': 'GET/POST', 'description': 'List seller products or create new ones'},
                {'name': 'Seller Orders', 'url': '/api/seller/orders/', 'method': 'GET', 'description': 'List orders for seller products'},
            ],
            'Payments': [
                {'name': 'List Payouts', 'url': '/api/payments/payouts/', 'method': 'GET/POST', 'description': 'List payouts or request a new one'},
                {'name': 'Payout Detail', 'url': '/api/payments/payouts/{id}/', 'method': 'GET', 'description': 'View a specific payout'},
            ],
            'Documentation': [
                {'name': 'Swagger UI', 'url': '/api/swagger/', 'method': 'GET', 'description': 'Interactive API documentation'},
                {'name': 'ReDoc', 'url': '/api/redoc/', 'method': 'GET', 'description': 'Alternative API documentation'},
            ],
            'Admin': [
                {'name': 'Admin Interface', 'url': '/admin/', 'method': 'GET', 'description': 'Django admin interface'},
            ]
        }
        
        return Response({
            'message': 'BazaarMate API Index',
            'description': 'Structured overview of all available API endpoints',
            'endpoints': endpoints
        })