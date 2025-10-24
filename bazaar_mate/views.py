from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

def home(request):
    """Render the home page"""
    return render(request, 'base/home.html')

def login_view(request):
    """Render the login page"""
    return render(request, 'auth/login.html')

def register_view(request):
    """Render the registration page"""
    return render(request, 'auth/register.html')

def product_list_view(request):
    """Render the product list page"""
    return render(request, 'products/product_list.html')

def product_detail_view(request):
    """Render the product detail page"""
    return render(request, 'products/product_detail.html')

def cart_view(request):
    """Render the cart page"""
    return render(request, 'cart/cart.html')

def orders_view(request):
    """Render the orders page"""
    return render(request, 'orders/orders.html')

def profile_view(request):
    """Render the profile page"""
    return render(request, 'profile/profile.html')

# API endpoints for frontend functionality
@csrf_exempt
def api_login(request):
    """Handle login via AJAX"""
    if request.method == 'POST':
        # This would normally call the DRF login endpoint
        # For now, we'll just return a mock response
        return JsonResponse({
            'success': True,
            'access': 'mock_access_token',
            'refresh': 'mock_refresh_token'
        })
    return JsonResponse({'success': False, 'error': 'Method not allowed'})

@csrf_exempt
def api_register(request):
    """Handle registration via AJAX"""
    if request.method == 'POST':
        # This would normally call the DRF register endpoint
        # For now, we'll just return a mock response
        return JsonResponse({
            'success': True,
            'message': 'User registered successfully'
        })
    return JsonResponse({'success': False, 'error': 'Method not allowed'})