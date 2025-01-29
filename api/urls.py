from django.urls import path
from .apiviews import (
    LoanRequestListView, LoanRequestDetailView,
    LendingOfferListView, LendingOfferDetailView
)

urlpatterns = [
    # Borrowing endpoints
    path('borrowing/', LoanRequestListView.as_view(), name='loan-request-list'),
    path('borrowing/<int:pk>/', LoanRequestDetailView.as_view(), name='loan-request-detail'),
    
    # Lending endpoints
    path('lending/', LendingOfferListView.as_view(), name='lending-offer-list'),
    path('lending/<int:pk>/', LendingOfferDetailView.as_view(), name='lending-offer-detail'),
]