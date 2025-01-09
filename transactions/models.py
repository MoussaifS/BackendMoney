from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# models.py
from django.core.validators import MinValueValidator

class LoanRequest(models.Model):
    LOAN_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('MODIFIED', 'Modified'),
        ('COMPLETED', 'Completed'),
        ('DEFAULTED', 'Defaulted')
    ]

    # Core fields
    borrower = models.ForeignKey(User, related_name='borrower_requests', on_delete=models.CASCADE)
    lender = models.ForeignKey(User, related_name='lender_requests', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Time related
    duration = models.DurationField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    
    # Financial
    total_payable = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Payment & Status
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=LOAN_STATUS)
    terms_accepted = models.BooleanField(default=False)
    
    # Documents
    receipt = models.FileField(upload_to='receipts/', null=True)
    contract_doc = models.FileField(upload_to='contracts/', null=True)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    purpose = models.TextField()
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['borrower', 'status']),
            models.Index(fields=['lender', 'status']),
        ]

    def __str__(self):
        return f"Loan request from {self.borrower.username} to {self.lender.username}"
    

    def clean(self):
        if not self.borrower or not self.lender:
            raise ValidationError('Both borrower and lender required')