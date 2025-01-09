# api/serializers.py
from rest_framework import serializers
from transactions.models import LoanRequest  # Change from .models

class LoanRequestSerializer(serializers.ModelSerializer):
   class Meta:
       model = LoanRequest
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