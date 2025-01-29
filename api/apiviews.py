from rest_framework import generics, permissions
from transactions.models import TransactionRequest
from .serializers import LenderSerializer, BorrowerSerializer

class LenderListView(generics.ListCreateAPIView):
    serializer_class = LenderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionRequest.objects.filter(lender=self.request.user)

    def perform_create(self, serializer):
        serializer.save(lender=self.request.user)

class BorrowerListView(generics.ListCreateAPIView):
    serializer_class = BorrowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return LoanRequest.objects.filter(borrower=self.request.user)
    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)
from rest_framework import generics, permissions
from transactions.models import TransactionRequest
from .serializers import TransactionRequestSerializer

class TransactionRequestListView(generics.ListCreateAPIView):
    serializer_class = TransactionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionRequest.objects.filter(borrower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)

class TransactionRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransactionRequest.objects.all()
    serializer_class = TransactionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

class LendingOfferListView(generics.ListCreateAPIView):
    serializer_class = LendingOfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LendingOffer.objects.all()

    def perform_create(self, serializer):
        serializer.save(lender=self.request.user)

class LendingOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LendingOffer.objects.all()
    serializer_class = LendingOfferSerializer
    permission_classes = [permissions.IsAuthenticated]