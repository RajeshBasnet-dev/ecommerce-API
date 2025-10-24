from django.urls import path
from .views import OrderMessageListView, MessageDetailView

urlpatterns = [
    path('orders/<int:order_id>/', OrderMessageListView.as_view(), name='order-message-list-create'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]