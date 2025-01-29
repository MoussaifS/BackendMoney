from django.contrib import admin
from .models import LendingOffer, LendingMatch

@admin.register(LendingOffer)
class LendingOfferAdmin(admin.ModelAdmin):
    list_display = ['lender', 'amount_offered', 'amount_remaining', 'status', 'publish_status', 'created_at']
    list_filter = ['status', 'publish_status']
    search_fields = ['lender__username']

@admin.register(LendingMatch)
class LendingMatchAdmin(admin.ModelAdmin):
    list_display = ['lending_offer', 'borrower', 'amount_requested', 'status', 'payment_status']
    list_filter = ['status', 'payment_status']
    search_fields = ['borrower__username']
