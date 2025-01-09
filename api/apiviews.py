from rest_framework import generics
from transactions.models import LoanRequest
from .serializers import LoanRequestSerializer

class LoanRequestListView(generics.ListCreateAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer