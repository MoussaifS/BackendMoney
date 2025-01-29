from django.conf import settings
from django.db import models

class LoanRequest(models.Model):
    REQUEST_STATUS = [
        ('PENDING', 'Pending'),
        ('MATCHED', 'Matched'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed')
    ]

    PUBLISH_STATUS = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    ]

    # Core fields
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_requests')
    amount_needed = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.TextField()
    preferred_term = models.DurationField()
    
    # Status fields
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='PENDING')
    publish_status = models.CharField(max_length=10, choices=PUBLISH_STATUS, default='PRIVATE')
    
    # Financial preferences
    amount_matched = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Documents and terms
    documents = models.FileField(upload_to='loan_documents/', null=True, blank=True)
    is_terms_accepted = models.BooleanField(default=False)
    credit_check_consent = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan request by {self.borrower.username} for {self.amount_needed} - {self.status}"

    def update_amount_matched(self, amount):
        """Update the matched amount when a lending offer is accepted"""
        self.amount_matched += amount
        if self.amount_matched >= self.amount_needed:
            self.status = 'MATCHED'
        self.save()

    def can_accept_offer(self, lending_offer):
        """Check if this request can accept a specific lending offer"""
        remaining_needed = self.amount_needed - self.amount_matched
        return (
            self.status == 'PENDING' and
            remaining_needed > 0 and
            (self.max_interest_rate is None or lending_offer.interest_rate <= self.max_interest_rate) and
            self.is_terms_accepted and
            self.credit_check_consent
        )
