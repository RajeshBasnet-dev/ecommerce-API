from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payout
from .serializers import PayoutSerializer

class PayoutListView(generics.ListCreateAPIView):
    serializer_class = PayoutSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payout.objects.all()
        elif user.role == 'seller':
            return Payout.objects.filter(seller__user=user)
        else:
            return Payout.objects.none()
    
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
        # Only admins can create payouts
        if request.user.role != 'admin':
            return Response({
                'success': False,
                'data': None,
                'error': 'Only admins can create payouts'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        }, status=status.HTTP_201_CREATED)

class PayoutDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PayoutSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payout.objects.all()
        elif user.role == 'seller':
            return Payout.objects.filter(seller__user=user)
        else:
            return Payout.objects.none()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'data': serializer.data,
            'error': None
        })
    
    def update(self, request, *args, **kwargs):
        # Only admins can update payouts
        if request.user.role != 'admin':
            return Response({
                'success': False,
                'data': None,
                'error': 'Only admins can update payouts'
            }, status=status.HTTP_403_FORBIDDEN)
        
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