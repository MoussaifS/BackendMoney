from django.shortcuts import render
from .models import TransactionRequest
from django.views.generic import ListView

class TransactionRequestListView(ListView):
    model = TransactionRequest
    template_name = 'transactionrequest_list.html'