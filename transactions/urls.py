from django.urls import path
from .views import TransactionRequestListView

urlpatterns = [
    path('', TransactionRequestListView.as_view(), name='home')
]

