from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import LendingOffer, LendingMatch
from .serializers import LendingOfferSerializer, LendingMatchSerializer

class LendingMatchCreate(generics.CreateAPIView):
    serializer_class = LendingMatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        lending_offer = serializer.validated_data['lending_offer']
        amount_requested = serializer.validated_data['amount_requested']
        
        if lending_offer.amount_remaining >= amount_requested:
            serializer.save(borrower=self.request.user)
        else:
            raise serializers.ValidationError("Requested amount exceeds available amount")
