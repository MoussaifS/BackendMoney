from django.urls import path
from .views import LoanRequestListView

urlpatterns = [
    path('', LoanRequestListView.as_view(), name='home')
]

