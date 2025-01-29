from rest_framework import serializers
from .models import LendingOffer, LendingMatch

class LendingMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LendingMatch
        fields = ['id', 'lending_offer', 'borrower', 'amount_requested', 
                 'status', 'payment_method', 'payment_status']
        read_only_fields = ['status', 'payment_status']

class LendingOfferSerializer(serializers.ModelSerializer):
    matches = LendingMatchSerializer(many=True, read_only=True, source='lendingmatch_set')
    
    class Meta:
        model = LendingOffer
        fields = ['id', 'amount_offered', 'amount_remaining', 'term_length',
                  'status', 'publish_status', 'requirements',
                 'terms_conditions', 'is_terms_accepted', 'matches']
        read_only_fields = ['lender', 'status', 'amount_remaining']