from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from lending.models import LendingOffer
from borrowing.models import LoanRequest

class TransactionRequest(models.Model):
    TRANSACTION_STATUS = [
        ('INITIATED', 'Initiated'),
        ('PAYMENT_PENDING', 'Payment Pending'),
        ('PAYMENT_COMPLETED', 'Payment Completed'),
        ('REJECTED', 'Rejected'),
        ('REFUNDED', 'Refunded')
    ]

    # Relationship fields
    lending_offer = models.ForeignKey(LendingOffer, on_delete=models.CASCADE, related_name='transactions')
    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE, related_name='transactions', null=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions_as_borrower')
    lender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions_as_lender')
    
    # Financial details
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    total_payable = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Payment details
    payment_method = models.CharField(max_length=50)
    payment_reference = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='INITIATED')
    
    # Time tracking
    duration = models.DurationField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Consent and verification
    borrower_consent = models.BooleanField(default=False)
    lender_consent = models.BooleanField(default=False)
    terms_accepted = models.BooleanField(default=False)
    
    # Documentation
    contract_doc = models.FileField(upload_to='contracts/', null=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['borrower', 'status']),
            models.Index(fields=['lender', 'status']),
            models.Index(fields=['lending_offer', 'status']),
        ]

    def __str__(self):
        return f"Transaction: {self.borrower.username} borrowing from {self.lender.username}"

    def clean(self):
        if not self.borrower or not self.lender:
            raise ValidationError('Both borrower and lender required')
        if self.borrower == self.lender:
            raise ValidationError('Borrower and lender cannot be the same user')

    @property
    def remaining_balance(self):
        return self.total_payable - self.amount_paid

    def can_proceed(self):
        return all([
            self.borrower_consent,
            self.lender_consent,
            self.terms_accepted,
            self.lending_offer.status == 'ACTIVE',
            self.lending_offer.amount_remaining >= self.amount_requested
        ])

    def process_payment(self, amount):
        if self.status != 'PAYMENT_PENDING':
            raise ValidationError('Transaction is not in payment pending state')
        if amount > self.remaining_balance:
            raise ValidationError('Payment amount exceeds remaining balance')
        
        self.amount_paid += amount
        if self.amount_paid >= self.total_payable:
            self.status = 'PAYMENT_COMPLETED'
        self.save()