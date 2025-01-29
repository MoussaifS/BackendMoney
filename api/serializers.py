# api/serializers.py
from rest_framework import serializers
from transactions.models import TransactionRequest
from lending.models import LendingOffer  # Add this import
from users.models import CustomUser

class LenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = (
            'id', 'borrower', 'amount', 'duration', 'start_date',
            'end_date', 'total_payable', 'status', 'terms_accepted',
            'lender_consent'
        )
        read_only_fields = ('borrower', 'status')

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = (
            'id', 'amount', 'duration', 'purpose', 'payment_method',
            'terms_accepted', 'borrower_consent'
        )

class TransactionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = (
            'id',
            'amount_needed',
            'purpose',
            'preferred_term',
            'status',
            'publish_status',
            'created_at',
            'documents',
            'is_terms_accepted'
        )

class LendingOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LendingOffer
        fields = (
            'id',
            'amount_offered',
            'term_length',
            'status',
            'created_at',
            'requirements',
            'terms_conditions',
            'is_terms_accepted'
        )
        read_only_fields = ('lender',)
        read_only_fields = ('borrower', 'status')

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = (
            'id', 'amount', 'duration', 'purpose', 'payment_method',
            'terms_accepted', 'borrower_consent'
        )

class TransactionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = (
            'id', 'borrower', 'lender', 'duration', 'start_date',
            'end_date', 'total_payable', 'amount_paid', 'status',
            'payment_method', 'borrower_consent', 'lender_consent',
            'terms_accepted'
        )
        read_only_fields = ('borrower', 'status')
    class Meta:
       model = TransactionRequest
       fields = (
           'id',
           'borrower',
           'lender', 
           'amount',
           'duration',
           'start_date',
           'end_date',
           'total_payable',
           'amount_paid',
           'payment_method',
           'status',
           'terms_accepted',
           'receipt',
           'contract_doc',
           'created_at',
           'updated_at',
           'purpose',
           'notes'
       )