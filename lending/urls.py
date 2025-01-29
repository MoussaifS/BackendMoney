from django.urls import path
from . import views

app_name = 'lending'

urlpatterns = [
    path('offers/', views.LendingOfferList.as_view(), name='offer-list'),
]