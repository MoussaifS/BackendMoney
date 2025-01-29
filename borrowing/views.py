from rest_framework import generics, permissions
from .models import LoanRequest
from .serializers import LoanRequestSerializer

class LoanRequestList(generics.ListCreateAPIView):
    serializer_class = LoanRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LoanRequest.objects.filter(borrower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)
