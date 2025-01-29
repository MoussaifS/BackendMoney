from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import LendingOffer

class LendingOfferTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.test_user = self.User.objects.create_user(
            username='testlender',
            password='testpass123',
            region='MY'
        )
        
        self.lending_offer = LendingOffer.objects.create(
            lender=self.test_user,
            amount_offered=Decimal('5000.00'),
            terms_conditions='Test terms and conditions',
            requirements='Test requirements',
            is_terms_accepted=True
        )

    def test_create_lending_offer(self):
        """Test creating a new lending offer"""
        self.assertEqual(self.lending_offer.amount_offered, Decimal('5000.00'))
        self.assertEqual(self.lending_offer.status, 'ACTIVE')
        self.assertEqual(self.lending_offer.lender, self.test_user)
        self.assertTrue(self.lending_offer.is_terms_accepted)

    def test_lending_offer_str(self):
        """Test the lending offer string representation"""
        expected_str = f"Lending offer by {self.test_user.username} - {self.lending_offer.amount_offered}"
        self.assertEqual(str(self.lending_offer), expected_str)

    def test_status_choices(self):
        """Test status field choices"""
        self.lending_offer.status = 'COMPLETED'
        self.lending_offer.save()
        self.assertEqual(self.lending_offer.status, 'COMPLETED')

    def test_invalid_status(self):
        """Test that invalid status raises error"""
        self.lending_offer.status = 'INVALID'
        with self.assertRaises(ValidationError):
            self.lending_offer.full_clean()

    def test_amount_offered_decimal(self):
        """Test amount_offered decimal field"""
        offer = LendingOffer.objects.create(
            lender=self.test_user,
            amount_offered=Decimal('1000.50'),
            terms_conditions='Test terms'
        )
        self.assertEqual(offer.amount_offered, Decimal('1000.50'))

    def test_blank_requirements(self):
        """Test that requirements field can be blank"""
        offer = LendingOffer.objects.create(
            lender=self.test_user,
            amount_offered=Decimal('1000.00'),
            terms_conditions='Test terms',
            requirements=''
        )
        self.assertEqual(offer.requirements, '')

    def test_auto_timestamp(self):
        """Test that created_at is automatically set"""
        self.assertIsNotNone(self.lending_offer.created_at)
