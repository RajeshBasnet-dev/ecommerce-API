from django.urls import path
from .views import PayoutListView, PayoutDetailView

urlpatterns = [
    path('payouts/', PayoutListView.as_view(), name='payout-list-create'),
    path('payouts/<int:pk>/', PayoutDetailView.as_view(), name='payout-detail'),
]