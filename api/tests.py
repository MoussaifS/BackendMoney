from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from borrowing.models import LoanRequest
from users.models import CustomUser

class LoanRequestAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123',
            region='MY'
        )
        self.client.force_authenticate(user=self.user)
        
        self.loan_data = {
            'amount_needed': '5000.00',
            'purpose': 'Business expansion',
            'preferred_term': '90 00:00:00',  # 90 days
            'publish_status': 'PUBLIC',
            'is_terms_accepted': True
        }

    def test_create_loan_request(self):
        response = self.client.post(
            reverse('loan-request-list'),
            self.loan_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanRequest.objects.count(), 1)
        self.assertEqual(LoanRequest.objects.get().amount_needed, 5000.00)

    def test_get_public_loans(self):
        # Create a public loan request
        LoanRequest.objects.create(**self.loan_data)
        
        # Create a private loan request
        private_loan = self.loan_data.copy()
        private_loan['publish_status'] = 'PRIVATE'
        LoanRequest.objects.create(**private_loan)

        response = self.client.get(
            f"{reverse('loan-request-list')}?public_only=true"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
