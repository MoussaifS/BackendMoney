from django.conf import settings
from django.db import models

class LendingOffer(models.Model):
    """
    Represents a lending offer created by a user (lender) who wants to lend money.
    Can be matched with multiple borrowers through LendingMatch.
    """
    OFFER_STATUS = [
        ('ACTIVE', 'Active'),      # Offer is available for borrowers
        ('MATCHED', 'Matched'),    # At least one borrower has been matched
        ('COMPLETED', 'Completed'), # All borrowed amounts have been repaid
        ('CANCELLED', 'Cancelled') # Offer was cancelled by the lender
    ]
    
    PUBLISH_STATUS = [
        ('PUBLIC', 'Public'),   # Visible to all users
        ('PRIVATE', 'Private'), # Visible only to specific users
    ]

    # Core relationship and amount fields
    lender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lending_offers')
    amount_offered = models.DecimalField(max_digits=10, decimal_places=2)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Loan terms
    term_length = models.DurationField()
    
    # Status and visibility
    status = models.CharField(max_length=20, choices=OFFER_STATUS, default='ACTIVE')
    publish_status = models.CharField(max_length=10, choices=PUBLISH_STATUS, default='PUBLIC')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Added update timestamp
    requirements = models.TextField(blank=True)
    terms_conditions = models.TextField()
    is_terms_accepted = models.BooleanField(default=False)
    
    # Relationship with borrowers through LendingMatch
    borrowers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='LendingMatch',
        related_name='borrowed_offers'
    )

    def save(self, *args, **kwargs):
        if self._state.adding:  # Only when creating new instance
            self.amount_remaining = self.amount_offered
        super().save(*args, **kwargs)

    def update_amount_remaining(self, amount_requested):
        """Update remaining amount after a successful match"""
        if self.amount_remaining >= amount_requested:
            self.amount_remaining -= amount_requested
            if self.amount_remaining == 0:
                self.status = 'COMPLETED'
            elif self.status == 'ACTIVE':
                self.status = 'MATCHED'
            self.save()
            return True
        return False

    def can_lend_to(self, borrower):
        """Check if the offer can be lent to a specific borrower"""
        return (
            self.status == 'ACTIVE' and
            borrower.credit_score >= self.min_credit_score and
            self.amount_remaining > 0
        )

    def __str__(self):
        return f"Lending offer by {self.lender.username} - {self.amount_offered}"

class LendingMatch(models.Model):
    """
    Represents a match between a lending offer and a borrower.
    Tracks the status of each individual loan and its payments.
    """
    MATCH_STATUS = [
        ('PENDING', 'Pending'),     # Borrower has requested to borrow
        ('APPROVED', 'Approved'),   # Lender has approved the request
        ('REJECTED', 'Rejected'),   # Lender has rejected the request
        ('COMPLETED', 'Completed')  # Loan has been fully repaid
    ]

    # Core relationships
    lending_offer = models.ForeignKey(LendingOffer, on_delete=models.CASCADE)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Loan details
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)  # Amount requested by borrower
    status = models.CharField(max_length=20, choices=MATCH_STATUS, default='APPROVED')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # When the match was created
    approved_at = models.DateTimeField(null=True, blank=True)  # When the lender approved
    
    # Payment information
    payment_method = models.CharField(max_length=50)  # Method of payment chosen by borrower
    payment_status = models.CharField(max_length=20, default='APPROVED')  # Status of payments
