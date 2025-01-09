from django.shortcuts import render
from .models import LoanRequest
from django.views.generic import ListView
# Create your views here.


class LoanRequestListView(ListView):
    model = LoanRequest
    template_name = 'loanrequest_list.html'