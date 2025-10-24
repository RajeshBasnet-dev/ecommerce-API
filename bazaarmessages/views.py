from django.db import models
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from orders.models import Order
from .serializers import MessageSerializer

class OrderMessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return Message.objects.filter(order_id=order_id)
    
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
        order_id = self.kwargs['order_id']
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({
                'success': False,
                'data': None,
                'error': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Determine receiver (should be the other party in the order)
        if request.user == order.user:
            # User is buyer, so receiver should be seller
            receiver = order.items.first().product.seller.user if order.items.exists() else None
        else:
            # User is seller, so receiver should be buyer
            receiver = order.user
        
        if not receiver:
            return Response({
                'success': False,
                'data': None,
                'error': 'Could not determine message recipient'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, receiver=receiver, order=order)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_201_CREATED)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(
            models.Q(sender=self.request.user) | models.Q(receiver=self.request.user)
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark as read if user is receiver
        if instance.receiver == request.user:
            instance.is_read = True
            instance.save()
        
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