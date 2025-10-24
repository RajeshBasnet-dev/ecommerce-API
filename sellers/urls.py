from django.urls import path
from .views import SellerProfileView, SellerProductListView, SellerOrderListView

urlpatterns = [
    path('profile/', SellerProfileView.as_view(), name='seller-profile'),
    path('products/', SellerProductListView.as_view(), name='seller-product-list-create'),
    path('orders/', SellerOrderListView.as_view(), name='seller-order-list'),
]