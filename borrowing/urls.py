from django.urls import path
from . import views

app_name = 'borrowing'

urlpatterns = [
    path('requests/', views.LoanRequestList.as_view(), name='request-list'),
]