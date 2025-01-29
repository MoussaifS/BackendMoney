from django.contrib import admin
from .models import LoanRequest

@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ['amount_needed', 'purpose', 'status', 'publish_status', 'created_at']
    list_filter = ['status', 'publish_status']
    search_fields = ['purpose']
