from django.urls import path
from .views import ProductReviewListCreateView, ReviewDetailView

urlpatterns = [
    path('products/<int:product_id>/', ProductReviewListCreateView.as_view(), name='product-review-list-create'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]