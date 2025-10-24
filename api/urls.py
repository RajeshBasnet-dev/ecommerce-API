from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="BazaarMate API",
      default_version='v1',
      description="API for BazaarMate e-commerce platform",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@bazaarmate.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Auth endpoints
    path('auth/', include('accounts.urls')),
    
    # Product endpoints
    path('products/', include('products.urls')),
    
    # Cart endpoints
    path('cart/', include('cart.urls')),
    
    # Order endpoints
    path('orders/', include('orders.urls')),
    
    # Review endpoints
    path('reviews/', include('reviews.urls')),
    
    # Wishlist endpoints
    path('wishlist/', include('wishlist.urls')),
    
    # Message endpoints
    path('messages/', include('bazaarmessages.urls')),
    
    # Payment endpoints
    path('payments/', include('payments.urls')),
    
    # Seller endpoints
    path('seller/', include('sellers.urls')),
]