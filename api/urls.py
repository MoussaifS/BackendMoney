from django.urls import path
from .apiviews import LoanRequestListView


urlpatterns = [
    path('', LoanRequestListView.as_view()),
]