from django.urls import path
from .views import WishlistView, AddToWishlistView, RemoveFromWishlistView

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist-detail'),
    path('add/', AddToWishlistView.as_view(), name='wishlist-add'),
    path('remove/', RemoveFromWishlistView.as_view(), name='wishlist-remove'),
]